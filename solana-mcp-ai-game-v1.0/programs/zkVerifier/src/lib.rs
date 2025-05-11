use anchor_lang::prelude::*;
use sha2::{Sha256, Digest};
use std::str::FromStr;

declare_id!("ZkVeri1111111111111111111111111111111111");

#[program]
pub mod zk_verifier {
    use super::*;

    /// Records a verified action from an agent to the blockchain
    /// @param agent_id - Unique identifier for the agent
    /// @param action_type - Type of action performed (enum as u8)
    /// @param data - JSON string of action data to hash
    /// @param timestamp - Unix timestamp when action occurred
    pub fn store_action(
        ctx: Context, 
        agent_id: String, 
        action_type: u8, 
        data: String,
        timestamp: i64
    ) -> Result {
        // Validate inputs
        require!(!agent_id.is_empty(), ErrorCode::InvalidAgentId);
        require!(!data.is_empty(), ErrorCode::EmptyActionData);
        require!(timestamp > 0, ErrorCode::InvalidTimestamp);
        
        // Check if action type is valid
        let action = match ActionType::from_u8(action_type) {
            Some(action) => action,
            None => return Err(ErrorCode::InvalidActionType.into())
        };
        
        // Get the current record
        let record = &mut ctx.accounts.record;
        
        // Initialize new record
        record.agent = agent_id;
        record.action_type = action_type;
        record.timestamp = timestamp;
        record.authority = ctx.accounts.user.key();
        
        // Hash the data
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        let hash = hasher.finalize();
        record.hash.copy_from_slice(&hash[..]);
        
        // Emit event for indexers
        emit!(ActionRecorded {
            record_id: record.key(),
            agent: record.agent.clone(),
            action_type,
            timestamp,
            authority: ctx.accounts.user.key(),
        });
        
        Ok(())
    }

    /// Verifies if provided data matches a stored hash
    /// Returns true if verification passes
    pub fn verify_action(ctx: Context, data: String) -> Result {
        // Verify data is not empty
        require!(!data.is_empty(), ErrorCode::EmptyActionData);
        
        // Hash input data
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        let input_hash = hasher.finalize();
        
        // Compare with stored hash
        let result = ctx.accounts.record.hash[..] == input_hash[..];
        
        // Emit verification event
        emit!(ActionVerified {
            record_id: ctx.accounts.record.key(),
            verified: result,
            verifier: ctx.accounts.user.key(),
        });
        
        Ok(result)
    }
    
    /// Allows an authority to update an action's metadata
    /// Cannot change the original hash to preserve integrity
    pub fn update_metadata(
        ctx: Context,
        new_metadata: String
    ) -> Result {
        // Only the original authority can update metadata
        require!(
            ctx.accounts.user.key() == ctx.accounts.record.authority,
            ErrorCode::UnauthorizedMetadataUpdate
        );
        
        // Store new metadata
        ctx.accounts.record.metadata = new_metadata;
        
        emit!(MetadataUpdated {
            record_id: ctx.accounts.record.key(),
            authority: ctx.accounts.user.key(),
        });
        
        Ok(())
    }
}

/// Represents the type of action an agent can perform
pub enum ActionType {
    Movement = 0,
    Interaction = 1,
    Crafting = 2,
    Combat = 3,
    Trading = 4,
    Quest = 5,
    // Add more action types here
}

impl ActionType {
    fn from_u8(value: u8) -> Option {
        match value {
            0 => Some(ActionType::Movement),
            1 => Some(ActionType::Interaction),
            2 => Some(ActionType::Crafting),
            3 => Some(ActionType::Combat),
            4 => Some(ActionType::Trading),
            5 => Some(ActionType::Quest),
            _ => None,
        }
    }
}

/// Action record stored on-chain
#[account]
#[derive(Debug)]
pub struct ActionRecord {
    pub agent: String,            // 64 bytes max
    pub action_type: u8,          // 1 byte
    pub hash: [u8; 32],           // 32 bytes
    pub timestamp: i64,           // 8 bytes
    pub authority: Pubkey,        // 32 bytes
    pub metadata: String,         // 128 bytes max
    // Total: ~265 bytes
}

/// Event emitted when a new action is recorded
#[event]
pub struct ActionRecorded {
    pub record_id: Pubkey,
    pub agent: String,
    pub action_type: u8,
    pub timestamp: i64,
    pub authority: Pubkey,
}

/// Event emitted when an action is verified
#[event]
pub struct ActionVerified {
    pub record_id: Pubkey,
    pub verified: bool,
    pub verifier: Pubkey,
}

/// Event emitted when metadata is updated
#[event]
pub struct MetadataUpdated {
    pub record_id: Pubkey,
    pub authority: Pubkey,
}

#[derive(Accounts)]
pub struct StoreAction {
    #[account(
        init,
        payer = user,
        space = 8 + 64 + 1 + 32 + 8 + 32 + 128
    )]
    pub record: Account,
    
    #[account(mut)]
    pub user: Signer,
    
    pub system_program: Program,
}

#[derive(Accounts)]
pub struct VerifyAction {
    pub record: Account,
    pub user: Signer,
}

#[derive(Accounts)]
pub struct UpdateMetadata {
    #[account(mut)]
    pub record: Account,
    
    pub user: Signer,
}

#[error_code]
pub enum ErrorCode {
    #[msg("Agent ID cannot be empty")]
    InvalidAgentId,
    
    #[msg("Action data cannot be empty")]
    EmptyActionData,
    
    #[msg("Invalid action type")]
    InvalidActionType,
    
    #[msg("Invalid timestamp")]
    InvalidTimestamp,
    
    #[msg("Only the original authority can update metadata")]
    UnauthorizedMetadataUpdate,
}
