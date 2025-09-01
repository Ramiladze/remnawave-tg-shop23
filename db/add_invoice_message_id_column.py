import asyncio
import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from config.settings import Settings

async def add_invoice_message_id_column():
    """Add invoice_message_id column to payments table if it doesn't exist."""
    settings = Settings()
    
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
    
    async with engine.begin() as conn:
        # Check if column already exists
        result = await conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'payments' AND column_name = 'invoice_message_id'
        """))
        
        if result.fetchone():
            logging.info("Column invoice_message_id already exists in payments table")
            return
        
        # Add the column
        await conn.execute(text("""
            ALTER TABLE payments 
            ADD COLUMN invoice_message_id BIGINT
        """))
        
        logging.info("Successfully added invoice_message_id column to payments table")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(add_invoice_message_id_column()) 