from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class DbUtils:
    
    session: AsyncSession= None
    
    @classmethod
    async def create(cls, session: AsyncSession):
        self= DbUtils()
        self.session= session
        return self

    async def get_list(self, model):
        """Retrieve a list of elements from database"""
        result = await self.session.execute(select(model))
        item_list = result.unique().scalars().all()
        return item_list


    async def get_list_statement_result(self, stmt):
        """Execute given statement and return list of items."""
        result = await self.session.execute(stmt)
        item_list = result.unique().scalars().all()
        return item_list


    async def get_element_statement_result(self, stmt):
        """Execute statement and return a single items"""
        result = await self.session.execute(stmt)
        item = result.scalar()
        return item


    async def get_element_by_id(self, model, element_id):
        """Retrieve any DB element by id."""
        if element_id is None:
            return None
        element = await self.session.get(model, element_id)
        return element

    # DELETE
    async def delete_element_by_id(self, model, element_id):
        """Delete any DB element by id."""
        element = await self.get_element_by_id(model, element_id)
        if element is not None:
            await self.session.delete(element)
            await self.session.commit()
        return element

    
    
    

        
