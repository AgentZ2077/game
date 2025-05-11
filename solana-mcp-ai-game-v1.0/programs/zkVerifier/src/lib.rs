
use anchor_lang::prelude::*;
use sha2::{Sha256, Digest};

declare_id!("ZkVeri1111111111111111111111111111111111");

#[program]
pub mod zk_verifier {
    use super::*;

    pub fn store_hash(ctx: Context<StoreHash>, agent: String, data: String) -> Result<()> {
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        let hash = hasher.finalize();
        ctx.accounts.record.hash.copy_from_slice(&hash[..]);
        ctx.accounts.record.agent = agent;
        Ok(())
    }

    pub fn verify_hash(ctx: Context<VerifyHash>, data: String) -> Result<bool> {
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        let hash = hasher.finalize();
        Ok(ctx.accounts.record.hash[..] == hash[..])
    }
}

#[account]
pub struct Record {
    pub agent: String,
    pub hash: [u8; 32],
}

#[derive(Accounts)]
pub struct StoreHash<'info> {
    #[account(init, payer = user, space = 8 + 32 + 64)]
    pub record: Account<'info, Record>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct VerifyHash<'info> {
    pub record: Account<'info, Record>,
}
