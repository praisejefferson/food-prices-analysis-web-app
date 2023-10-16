import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

st.set_page_config(page_title="Africa food prices",
                  page_icon=":bar_chart:",
                  layout="wide"
)

hide_st_style = """
<style>
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)


@st.cache_data
def load_data():
    df=pd.read_csv("python/datasets/africa_food_prices.csv")
    df.head()
    def fill_nulls(row):
        if pd.isnull(row["state"]):
            return row["market"]
        else:
            return row["state"]
    df["state"] = df.apply(fill_nulls, axis=1)
    df["state"] = df.apply(fill_nulls, axis=1)
    df.drop(columns=df.columns[-1], inplace=True)
    df.drop(columns = ["currency_id"], inplace = True)
    df=df.rename(columns={"country_id":"Country_ID","country":"Country","state_id":"State_ID",
                    "state":"State","market_id":"Market_ID","market":"Market","produce_id":"Produce_ID",
                    "produce":"Produce", "currency":"Currency",
                    "pt_id ":"PT_ID","market_type":"Market_Type","um_unit_id":"Quantity",
                     "quantity":"Um_Unit_ID","month":"Month","year":"Year","price":"Price"})
  
    
    return df
    
def calculate_revenue_by_country(df):
    df['Revenue'] = df['Price'] * df['Quantity']
    revenue_by_country = df.groupby('Country')['Revenue'].sum().nlargest(10)
    return revenue_by_country


def price_quantity_by_type(df):
    df['Date'] = pd.to_datetime(df['Date'])
    price_by_time = df.groupby(['Date', 'Market_Type'])[['Price', 'Quantity']].mean().reset_index()
    return price_by_time
    
    
def main():
    
    st.title(":bar_chart: AFRICA FOOD SALES DASHBOARD")
    st.markdown("##")
    
    df = load_data()
    st.sidebar.header("Please Enter Filter")
    Country = df['Country'].unique()
    Country_selection = st.sidebar.multiselect('Choose Country', Country, [Country[0], Country[1]])
    Country_selected = df[df["Country"].isin(Country_selection)]
    
    
    State = df['State'].unique()
    State_selection = st.sidebar.multiselect('Choose state', State, [State[0], State[1]])
    State_selected = df[df["State"].isin(State_selection)]
    
    col1, col2, col3 = st.columns(3)


    total_state = df['State_ID'].nunique()
    average_price = df['Price'].mean()
    total_countries = df['Country_ID'].nunique()

    with col1:
        st.markdown(f"### State\n{total_state}")       
        st.write("Total States")
    with col2:
        st.markdown(f"### Average Price\n${average_price:,.0f}")         
        st.write("Average Price")                                             
    with col3:
        st.markdown(f"### Country\n{total_countries}")          
        st.write("Total Countries")
    st.markdown("---")  
    st.write("")
    
    
    col1, col2 = st.columns([1, 1])  # Adjust column widths as needed

    with col1:
        top_countries = df['Country'].value_counts().head(10).sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(9, 6))  # Adjust the figsize for the first chart
        ax.bar(top_countries.index, top_countries.values)
        plt.xticks(rotation=45)
        plt.xlabel('Country')
        plt.ylabel('Count')
        plt.title('Top 10 African Countries With Most Market Activities')
        st.pyplot(fig)
        st.write("")

    with col2:
        revenue_data = calculate_revenue_by_country(df)
        fig, ax = plt.subplots(figsize=(9, 6))  # Adjust the figsize for the second chart
        ax.barh(revenue_data.index, revenue_data.values, color='purple')
        plt.xticks(rotation=45)
        plt.xlabel('Country')
        plt.ylabel('Revenue')
        plt.title("Top 10 Countries by Revenue")
        st.pyplot(fig)
        st.write("")
        
        
    price_quantity_data = price_quantity_by_type
    st.pyplot(plt.figure(figsize=(12, 8)))

    
    plt.subplot(2, 1, 1)
    for market_type, data in price_quantity_data.groupby('Market_Type'):
        plt.plot(data['Date'], data['Price'], label=market_type)
        plt.title('Price Over Time by Market Type')
        plt.xlabel('Date')
        plt.ylabel('Average Price')
        plt.xticks(rotation=45)
        plt.legend(title='Market Type')


    plt.subplot(2, 1, 2)
    for market_type, data in price_quantity_data.groupby('Market_Type'):
        plt.plot(data['Date'], data['Quantity'], label=market_type)
        plt.title('Quantity Sold Over Time by Market Type')
        plt.xlabel('Date')
        plt.ylabel('Average Quantity Sold')
        plt.xticks(rotation=45)
        plt.legend(title='Market Type')
        
        
        
if __name__ == '__main__':
    main()
                             


            
            
