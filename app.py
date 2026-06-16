import streamlit as st
import pandas as pd
import os

# Set page config for a wide layout, premium title, and app icon
st.set_page_config(
    page_title="Food Delivery Transactions Explorer",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject modern styling with custom CSS for high-fidelity aesthetics
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Font style override */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Sleek gradient background header */
    .hero-container {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 60%);
        transform: rotate(15deg);
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        font-weight: 300;
        opacity: 0.9;
        margin-top: 0.5rem;
        line-height: 1.6;
    }
    
    /* Custom metric card cards styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.15);
        border-color: rgba(124, 58, 237, 0.3);
    }
    
    .metric-val {
        font-size: 1.75rem;
        font-weight: 800;
        color: #7C3AED;
    }
    
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #71717a;
        margin-top: 0.25rem;
        font-weight: 600;
    }
    
    /* Section Headings */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-left: 0.5rem;
        border-left: 4px solid #7C3AED;
        color: inherit;
    }
    
    /* Styled footer */
    .footer-text {
        text-align: center;
        color: #a1a1aa;
        font-size: 0.85rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data helper cached to maximize load speed performance
@st.cache_data
def load_data():
    file_path = "synthetic_food_delivery_transactions.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        return None

# Load dataset
df = load_data()

# Render Landing Header Hero
st.markdown(
    """
    <div class="hero-container">
        <h1 class="hero-title">🍔 Food Delivery Dashboard</h1>
        <p class="hero-subtitle">Interactive analysis of customer orders, restaurants, prep times, and transaction values.</p>
    </div>
    """,
    unsafe_allow_html=True
)

if df is not None:
    # Sidebar Configuration & Filters
    with st.sidebar:
        st.markdown("### 🛠️ Dashboard Configuration")
        st.write("Easily adjust visual options and explore dataset characteristics.")
        
        # Interactive slider to change number of rows (default 5)
        num_rows = st.slider(
            "Rows to preview",
            min_value=1,
            max_value=50,
            value=5,
            help="Choose the number of records to show in the preview table below."
        )
        
        st.markdown("---")
        st.markdown("### 📊 Dataset Overview")
        st.markdown(f"**Total Records:** `{len(df):,}`")
        st.markdown(f"**Total Columns:** `{len(df.columns)}`")
        
        # Simple filter by City
        all_cities = sorted(df['restaurant_city'].dropna().unique())
        selected_cities = st.multiselect(
            "Filter by City",
            options=all_cities,
            default=[]
        )
        
        # Simple filter by Cuisine
        all_cuisines = sorted(df['restaurant_cuisine'].dropna().unique())
        selected_cuisines = st.multiselect(
            "Filter by Cuisine",
            options=all_cuisines,
            default=[]
        )

    # Filter dataframe based on selections
    filtered_df = df
    if selected_cities:
        filtered_df = filtered_df[filtered_df['restaurant_city'].isin(selected_cities)]
    if selected_cuisines:
        filtered_df = filtered_df[filtered_df['restaurant_cuisine'].isin(selected_cuisines)]

    # Key Statistics Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-val">{len(filtered_df):,}</div>
                <div class="metric-label">Filtered Orders</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        avg_val = filtered_df['total_amount'].mean() if len(filtered_df) > 0 else 0
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-val">${avg_val:.2f}</div>
                <div class="metric-label">Avg Order Amount</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col3:
        avg_rating = filtered_df['restaurant_rating'].mean() if len(filtered_df) > 0 else 0
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-val">★ {avg_rating:.2f}</div>
                <div class="metric-label">Avg Restaurant Rating</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col4:
        avg_prep = filtered_df['restaurant_avg_prep_time'].mean() if len(filtered_df) > 0 else 0
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-val">{avg_prep:.1f} min</div>
                <div class="metric-label">Avg Prep Time</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual Insights Section
    st.markdown('<div class="section-title">Visual Insights</div>', unsafe_allow_html=True)
    
    col_chart, col_info = st.columns([2, 1])
    
    with col_chart:
        st.markdown("### 🏆 Top 10 Most Popular Cuisines")
        if len(filtered_df) > 0:
            cuisine_counts = filtered_df['restaurant_cuisine'].value_counts().head(10).reset_index()
            cuisine_counts.columns = ['Cuisine', 'Order Volume']
            st.bar_chart(
                data=cuisine_counts,
                x='Cuisine',
                y='Order Volume',
                color='#7C3AED',
                use_container_width=True
            )
        else:
            st.warning("No data available for the selected filters.")
            
    with col_info:
        st.markdown("### 💡 Quick Insights")
        if len(filtered_df) > 0:
            top_cuisine = filtered_df['restaurant_cuisine'].mode()[0]
            top_cuisine_count = filtered_df['restaurant_cuisine'].value_counts().iloc[0]
            st.markdown(f"- The most popular cuisine is **{top_cuisine}** with **{top_cuisine_count:,}** orders.")
            st.markdown(f"- Cuisines are sorted by total transaction frequency.")
            st.markdown(f"- Adjust filters in the sidebar to recalculate popularity by city.")
        else:
            st.write("No insights available.")

    st.markdown("---")
    st.markdown("### 📈 Daily Revenue Timeline")
    if len(filtered_df) > 0:
        # Copy to avoid SettingWithCopy warning and compute daily totals
        revenue_df = filtered_df.copy()
        revenue_df['Date'] = pd.to_datetime(revenue_df['order_timestamp']).dt.date
        daily_revenue = revenue_df.groupby('Date')['total_amount'].sum().reset_index()
        daily_revenue.columns = ['Date', 'Daily Revenue']
        daily_revenue = daily_revenue.sort_values('Date')
        
        st.line_chart(
            data=daily_revenue,
            x='Date',
            y='Daily Revenue',
            color='#EC4899',
            use_container_width=True
        )
    else:
        st.warning("No data available for the selected filters.")

    st.markdown("---")
    
    # Scatter Plot row
    col_scatter, col_scatter_info = st.columns([2, 1])
    
    with col_scatter:
        st.markdown("### ☀️ Weather vs. Actual Delivery Duration")
        if len(filtered_df) > 0:
            # Clean null values for temperature and duration
            scatter_df = filtered_df.dropna(subset=['weather_temperature', 'delivery_duration_actual'])
            st.scatter_chart(
                data=scatter_df,
                x='weather_temperature',
                y='delivery_duration_actual',
                color='#4F46E5',
                use_container_width=True
            )
        else:
            st.warning("No data available for the selected filters.")
            
    with col_scatter_info:
        st.markdown("### ❄️ Weather Delay Analysis")
        if len(filtered_df) > 0:
            scatter_df = filtered_df.dropna(subset=['weather_temperature', 'delivery_duration_actual'])
            if len(scatter_df) > 1:
                correlation = scatter_df['weather_temperature'].corr(scatter_df['delivery_duration_actual'])
                st.markdown(f"- **Correlation Coefficient:** `{correlation:.3f}`")
                if abs(correlation) < 0.1:
                    relation_desc = "virtually no linear relationship"
                elif correlation > 0:
                    relation_desc = "a slight positive correlation (higher temps = longer delivery)"
                else:
                    relation_desc = "a slight negative correlation (colder temps = longer delivery)"
                st.markdown(f"- There is {relation_desc} between temperature and delivery duration in the selected subset.")
            
            avg_duration = filtered_df['delivery_duration_actual'].mean()
            st.markdown(f"- **Average Delivery Duration:** `{avg_duration:.1f} minutes`")
            st.markdown(f"- Use this scatter plot to identify outliers (e.g. extremely long delivery times in cold or stormy weather).")
        else:
            st.write("No analysis available.")

    st.markdown("---")
    
    # Pie/Donut Chart row
    col_pie, col_pie_info = st.columns([2, 1])
    
    with col_pie:
        st.markdown("### 🏆 Orders by Customer Loyalty Tier")
        if len(filtered_df) > 0:
            import altair as alt
            
            # Count orders by loyalty tier
            loyalty_counts = filtered_df['customer_loyalty_tier'].value_counts().reset_index()
            loyalty_counts.columns = ['Loyalty Tier', 'Orders']
            
            # Create a styled donut chart in Altair
            donut_chart = alt.Chart(loyalty_counts).mark_arc(innerRadius=60, outerRadius=110).encode(
                theta=alt.Theta(field="Orders", type="quantitative"),
                color=alt.Color(field="Loyalty Tier", type="nominal", scale=alt.Scale(
                    domain=['Gold', 'Silver', 'Bronze'],
                    range=['#F59E0B', '#94A3B8', '#D97706'] # Polished Gold, Silver/Slate, Bronze/Orange
                ), legend=alt.Legend(title="Loyalty Tier")),
                tooltip=['Loyalty Tier', 'Orders']
            ).properties(
                height=280
            )
            
            st.altair_chart(donut_chart, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")
            
    with col_pie_info:
        st.markdown("### 💎 Loyalty Tier Insights")
        if len(filtered_df) > 0:
            loyalty_counts = filtered_df['customer_loyalty_tier'].value_counts()
            total_loyalty_orders = loyalty_counts.sum()
            
            st.markdown(f"- **Total Loyalty Program Orders:** `{total_loyalty_orders:,}`")
            
            for tier in ['Gold', 'Silver', 'Bronze']:
                if tier in loyalty_counts:
                    count = loyalty_counts[tier]
                    percentage = (count / total_loyalty_orders) * 100
                    # Calculate average order value for this tier
                    tier_df = filtered_df[filtered_df['customer_loyalty_tier'] == tier]
                    avg_spend = tier_df['total_amount'].mean() if len(tier_df) > 0 else 0
                    
                    st.markdown(
                        f"- **{tier} Tier:** `{percentage:.1f}%` of orders "
                        f"({count:,} orders), averaging **${avg_spend:.2f}** per order."
                    )
        else:
            st.write("No analysis available.")

    st.markdown("---")
    
    # Heatmap row
    col_heat, col_heat_info = st.columns([2, 1])
    
    with col_heat:
        st.markdown("### 📊 Correlation Heatmap")
        if len(filtered_df) > 0:
            import altair as alt
            
            # Map column names for display
            cols_map = {
                'restaurant_avg_prep_time': 'Prep Time',
                'delivery_fee': 'Delivery Fee',
                'tip': 'Tip Amount',
                'delivery_duration_actual': 'Delivery Duration'
            }
            
            # Drop null values and calculate correlation matrix
            heat_df = filtered_df[list(cols_map.keys())].dropna().rename(columns=cols_map)
            
            if len(heat_df) > 1:
                corr_matrix = heat_df.corr()
                corr_data = corr_matrix.stack().reset_index()
                corr_data.columns = ['Variable 1', 'Variable 2', 'Correlation']
                
                # Base chart
                base = alt.Chart(corr_data).encode(
                    x=alt.X('Variable 1:N', title=None),
                    y=alt.Y('Variable 2:N', title=None)
                )
                
                # Heatmap rectangles
                heatmap = base.mark_rect().encode(
                    color=alt.Color('Correlation:Q', scale=alt.Scale(scheme='viridis', domain=[-1, 1]), title="Corr"),
                    tooltip=['Variable 1', 'Variable 2', alt.Tooltip('Correlation:Q', format='.3f')]
                )
                
                # Correlation values as text overlay
                text = base.mark_text(fontSize=14, fontWeight='bold').encode(
                    text=alt.Text('Correlation:Q', format='.3f'),
                    color=alt.condition(
                        alt.datum.Correlation > 0.5,
                        alt.value('black'),
                        alt.value('white')
                    )
                )
                
                st.altair_chart(heatmap + text, use_container_width=True)
            else:
                st.warning("Not enough data to calculate correlations.")
        else:
            st.warning("No data available for the selected filters.")
            
    with col_heat_info:
        st.markdown("### 🔍 Correlation Insights")
        if len(filtered_df) > 0:
            heat_df = filtered_df[list(cols_map.keys())].dropna().rename(columns=cols_map)
            if len(heat_df) > 1:
                corr_matrix = heat_df.corr()
                
                # Extract interesting correlations
                prep_duration_corr = corr_matrix.loc['Prep Time', 'Delivery Duration']
                fee_duration_corr = corr_matrix.loc['Delivery Fee', 'Delivery Duration']
                
                st.markdown(f"- **Prep Time vs. Delivery Duration:** `{prep_duration_corr:.3f}`")
                st.markdown(f"- **Delivery Fee vs. Delivery Duration:** `{fee_duration_corr:.3f}`")
                st.markdown("---")
                st.markdown("**Interpretation Guide:**")
                st.markdown("- `+1.000` = Perfect positive relationship.")
                st.markdown("- `0.000` = No linear relationship.")
                st.markdown("- `-1.000` = Perfect negative relationship.")
                st.markdown("- Higher correlation between *Prep Time* and *Delivery Duration* implies prep delays directly prolong the customer's wait.")
            else:
                st.write("Not enough data.")
        else:
            st.write("No insights available.")

    st.markdown("<br>", unsafe_allow_html=True)

    # DataFrame display section
    st.markdown(f'<div class="section-title">Dataset Preview (Showing first {num_rows} records)</div>', unsafe_allow_html=True)
    
    # Render the styled DataFrame
    st.dataframe(
        filtered_df.head(num_rows),
        use_container_width=True,
        hide_index=True
    )

    # Quick download button for current selection
    st.markdown("<br>", unsafe_allow_html=True)
    csv_data = filtered_df.head(num_rows).to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download current preview as CSV",
        data=csv_data,
        file_name="delivery_transactions_preview.csv",
        mime="text/csv",
    )

else:
    st.error("⚠️ Unable to load the dataset. Please ensure `synthetic_food_delivery_transactions.csv` exists in the application directory.")

# Dashboard footer
st.markdown(
    """
    <div class="footer-text">
        Designed for Food Delivery Analytics Dashboard &copy; 2026. Built with Streamlit.
    </div>
    """,
    unsafe_allow_html=True
)
