import streamlit as st
from st_xatadb_connection  import XataConnection
import asyncio



class DBmanager:
    def __init__(self):
        self.xata = st.connection('xata',type=XataConnection)


    async def _get_user(self,identifier):
        return self.xata.get("Usuario",identifier)

    async def get_user(self,identifier):
        result =  await self._get_user(identifier)
        return result

    async def _insert_user(self,data,identifier=None):
        return self.xata.insert("Usuario",data,identifier)

    async def insert_user(self,data,identifier=None):
        result = await self._insert_user(data,identifier)
        return result

    def get(self,table,identifier):
        if table == "Usuario":
            return asyncio.run(self.get_user(identifier))

    def insert(self,table,data,identifier=None):
        if table == "Usuario":
            return asyncio.run(self.insert_user(data,identifier))

