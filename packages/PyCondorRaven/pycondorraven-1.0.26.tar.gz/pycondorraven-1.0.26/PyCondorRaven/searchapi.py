import pandas as pd
from langchain.agents import load_tools, initialize_agent
import ast

class search_engine:
    def __init__(self, model):
        tools = load_tools(["google-serper"])
        self.agent = initialize_agent(tools, model, agent="zero-shot-react-description", verbose=False)

    def assets(self, assets_array, prompt=None):
        if prompt is None:
            self.search_asset_prompt = """
            Please look up the instrument %s with ISIN %s and provide the details in the following format:
            {
            'Asset class': 'Equity/Bond/Money Market/Alternatives/Other',
            'Currency': 'USD/EUR/Other',
            'Country': 'ISO code (e.g., US, FR)'
            'Market': 'emerging markets/developed markets/Other',
            'Rating': 'government bond/high yield/investment grade/Other'
            'Type': 'stock/bond/derivative/fund/other'
            }
            """
        else:
            self.search_asset_prompt = prompt

        items = []
        for item in assets_array:
            print(f"Searching {item['id']} with isin {item['isin']}")
            try:
                response = self.agent.run(self.search_asset_prompt % (item['id'], item['isin']))
                item = {**{'Isin':item['isin'], 'Name':item['id']}, **ast.literal_eval(response)}
            except Exception as e:
                item = {'Isin':item['isin'], 'Name':item['id'], 'Asset class':'', 'Currency':'', 'Country':'', 'Market':'', 'Rating':''}
                print(f'Cannot identify instrument:{str(e)}')
            items.append(item)
        
        return pd.DataFrame(items)