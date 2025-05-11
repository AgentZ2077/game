
use anchor_lang::prelude::*;

declare_id!("ZkMemVer1111111111111111111111111111111111");

#[program]
pub mod zk_verifier {
    use super::*;

    pub fn store_memory_hash(ctx: Context<StoreHash>, hash: [u8; 32]) -> Result<()> {
        let memory = &mut ctx.accounts.memory;
        memory.hash = hash;
        Ok(())
    }

    pub fn verify_proof(ctx: Context<VerifyProof>, provided: [u8; 32]) -> Result<()> {
        let memory = &ctx.accounts.memory;
        require!(memory.hash == provided, ZkError::InvalidProof);
        Ok(())
    }
}

#[derive(Accounts)]
pub struct StoreHash<'info> {
    #[account(init_if_needed, payer = signer, space = 8 + 32, seeds = [b"memory", signer.key().as_ref()], bump)]
    pub memory: Account<'info, Memory>,
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct VerifyProof<'info> {
    #[account(seeds = [b"memory", signer.key().as_ref()], bump)]
    pub memory: Account<'info, Memory>,
    pub signer: Signer<'info>,
}

#[account]
pub struct Memory {
    pub hash: [u8; 32],
}

#[error_code]
pub enum ZkError {
    #[msg("The proof is invalid.")]
    InvalidProof,
}
