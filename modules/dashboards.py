import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

def run():
    # Data source selection: CSV (offline) or Snowflake (cloud)
    use_snowflake = False
    if 'offline_mode' in st.session_state:
        use_snowflake = not st.session_state['offline_mode']
    st.sidebar.markdown('---')
    st.sidebar.write('**Data Source:**')
    data_source = st.sidebar.radio('Choose data source:', ['Local CSV', 'Snowflake (Cloud)'],
                                   index=0, key='dash_data_source',
                                   help='Snowflake is not implemented in this demo. Only Local CSV is available.')
    use_snowflake = False  # Always use CSV, Snowflake not implemented

    st.title("Responsible Cultural Tourism")
    st.markdown("""
    Explore how tourism impacts cultural preservation and learn how to be a responsible 
    cultural tourist. This section provides data-driven insights on sustainable tourism 
    practices and their effects on local communities and cultural heritage.
    """)

    # Tabs for different aspects of responsible tourism
    tab1, tab2, tab3, tab4 = st.tabs([
        "Impact Analysis", 
        "Sustainable Practices", 
        "Community Benefits", 
        "Responsible Tourism Pledge"
    ])

    # --- Impact Analysis Tab ---
    with tab1:
        st.header("Tourism Impact on Cultural Heritage")
        st.markdown("""
        This analysis explores how tourism affects cultural heritage sites and traditions, 
        using data to identify both positive and negative impacts.
        """)
        # Load impact metrics from CSV
        impact_path = os.path.join(os.path.dirname(__file__), '../data/tourism_impact_metrics.csv')
        impact_df = pd.read_csv(impact_path)
        impact_col1, impact_col2 = st.columns(2)
        with impact_col1:
            st.subheader("Positive Impacts")
            pos = impact_df[impact_df['impact_type']=='positive']
            fig = px.bar(
                x=pos['category'],
                y=pos['score'],
                color=pos['score'],
                color_continuous_scale='Greens',
                title="Positive Impacts of Tourism on Cultural Heritage",
                labels={'x': 'Impact Category', 'y': 'Impact Score (0-100)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        with impact_col2:
            st.subheader("Negative Impacts")
            neg = impact_df[impact_df['impact_type']=='negative']
            fig = px.bar(
                x=neg['category'],
                y=neg['score'],
                color=neg['score'],
                color_continuous_scale='Reds',
                title="Negative Impacts of Tourism on Cultural Heritage",
                labels={'x': 'Impact Category', 'y': 'Impact Score (0-100)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        # Case studies
        st.subheader("Impact Case Studies")
        
        case_col1, case_col2, case_col3 = st.columns(3)
        
        with case_col1:
            st.markdown("### Jaipur Block Printing")
            st.image("https://www.sundarisilks.com/cdn/shop/articles/gems-of-jaipur-sundari-silks-blog-cover_2400x600.jpg?height=200&width=300", caption="Traditional Block Printing")
            st.markdown("""
            **Positive Impact**: Tourism has revived this traditional craft, providing economic support to artisan families.
            
            **Challenge**: Mass production of "tourist" versions has led to quality concerns.
            """)
        
        with case_col2:
            st.markdown("### Khajuraho Temples")
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRh5H4DZ_TYMQ4wH9ScXsyyie9mn5vS3t1Ppw&s&height=200&width=300", caption="Khajuraho Temple Sculptures")
            st.markdown("""
            **Positive Impact**: Tourism funding has supported preservation efforts.
            
            **Challenge**: High visitor numbers have led to physical degradation of some structures.
            """)
            
        with case_col3:
            st.markdown("### Kutch Embroidery")
            st.image("https://m.media-amazon.com/images/I/91QkFQfMgrL.jpg?height=200&width=300", caption="Kutch Embroidery")
            st.markdown("""
            **Positive Impact**: Craft has gained international recognition through tourism.
            
            **Challenge**: Some designs have been commercialized without proper attribution.
            """)
    
    # --- Sustainable Practices Tab ---
    with tab2:
        st.header("Sustainable Tourism Practices")
        st.markdown("""
        Learn how to enjoy cultural experiences while minimizing negative impacts and 
        maximizing benefits to local communities and cultural preservation.
        """)
        st.subheader("Responsible Cultural Tourism Best Practices")
        practices_col1, practices_col2 = st.columns(2)
        with practices_col1:
            st.markdown("""
            ### Before Your Visit
            - **Research cultural norms** and appropriate behavior
            - **Learn a few phrases** in the local language
            - **Choose community-based accommodations** where possible
            - **Pack responsibly** with minimal waste
            - **Plan visits to lesser-known sites** to reduce overtourism
            ### During Your Visit
            - **Respect photography guidelines** at cultural sites
            - **Ask permission before photographing** people or private ceremonies
            - **Participate in authentic cultural experiences** led by local experts
            - **Support artisans by purchasing directly** from them
            - **Use local guides** who can provide cultural context
            """)
        with practices_col2:
            # Load practices metrics from CSV
            practices_path = os.path.join(os.path.dirname(__file__), '../data/tourism_practices_metrics.csv')
            practices_df = pd.read_csv(practices_path)
            categories = practices_df['practice'].tolist()
            values = practices_df['score'].tolist()
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Impact Score'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                title="Impact of Responsible Tourism Practices"
            )
            st.plotly_chart(fig, use_container_width=True)
        # Sustainable tourism indicators
        st.subheader("Sustainable Tourism Indicators by Region")
        sustainability_path = os.path.join(os.path.dirname(__file__), '../data/tourism_sustainability_indicators.csv')
        sustainability_data = pd.read_csv(sustainability_path)
        fig = px.imshow(
            sustainability_data.set_index('region'),
            text_auto=True,
            color_continuous_scale='Greens',
            title="Sustainable Tourism Performance by Region"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Sustainable initiatives
        st.subheader("Highlighted Sustainable Tourism Initiatives")
        
        initiative_col1, initiative_col2, initiative_col3 = st.columns(3)
        
        with initiative_col1:
            st.markdown("### Village Homestay Program")
            st.image("https://etimg.etb2bimg.com/photo/78378695.cms?height=150&width=250", caption="Rural Homestay")
            st.markdown("""
            Community-run homestays that provide authentic cultural experiences while ensuring tourism benefits go directly to local families.
            
            **Impact**: 500+ families supported across 75 villages
            """)
        
        with initiative_col2:
            st.markdown("### Heritage Craft Schools")
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_twVP815F26xshFi82Xg8zvq2wE1Y7uU88Q&s&height=150&width=250", caption="Craft Training")
            st.markdown("""
            Programs that teach traditional crafts to younger generations, funded partly by tourism revenues and workshops.
            
            **Impact**: 15 endangered crafts preserved through 30+ schools
            """)
            
        with initiative_col3:
            st.markdown("### Cultural Site Management")
            st.image("https://dronah.org/wp-content/uploads//2017/02/909885.jpg?height=150&width=250", caption="Site Conservation")
            st.markdown("""
            Community-led management of cultural sites that balances preservation with sustainable tourism.
            
            **Impact**: 40% reduction in site degradation at participating locations
            """)
    
    # --- Community Benefits Tab ---
    with tab3:
        st.header("Community Benefits Analysis")
        st.markdown("""
        Explore how cultural tourism can directly benefit local communities when practiced responsibly, 
        based on data from cultural sites across India.
        """)
        st.subheader("Economic Impact of Cultural Tourism")
        econ_path = os.path.join(os.path.dirname(__file__), '../data/tourism_community_economics.csv')
        econ_df = pd.read_csv(econ_path)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=econ_df['year'],
            y=econ_df['community_revenue'],
            name="Direct Community Revenue",
            marker_color='green'
        ))
        fig.add_trace(go.Bar(
            x=econ_df['year'],
            y=econ_df['corporate_revenue'],
            name="Corporate Tourism Revenue",
            marker_color='blue'
        ))
        fig.add_trace(go.Scatter(
            x=econ_df['year'],
            y=econ_df['artisan_income'],
            name="Avg. Artisan Annual Income",
            yaxis="y2",
            line=dict(color='red', width=3)
        ))
        fig.update_layout(
            title="Economic Impact of Cultural Tourism (2018-2023)",
            yaxis=dict(title="Revenue (Millions USD)", side="left"),
            yaxis2=dict(title="Artisan Income (Thousands USD)", side="right", overlaying="y", range=[0, 10]),
            barmode='group',
            legend=dict(x=0.01, y=0.99),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Community Benefits Breakdown")
        benefits_path = os.path.join(os.path.dirname(__file__), '../data/tourism_community_benefits.csv')
        benefits_df = pd.read_csv(benefits_path)
        benefits_col1, benefits_col2 = st.columns(2)
        with benefits_col1:
            fig = px.pie(
                values=benefits_df['percent'],
                names=benefits_df['benefit'],
                title="Distribution of Cultural Tourism Benefits",
                color_discrete_sequence=px.colors.sequential.Greens
            )
            st.plotly_chart(fig, use_container_width=True)
        with benefits_col2:
            st.markdown("### Success Metrics from Community-Based Tourism")
            st.metric("Artisan Income Increase", "+45%", "vs. non-tourism communities")
            st.metric("Youth Engagement in Cultural Practices", "+30%", "in tourism-supported communities")
            st.metric("Cultural Preservation Investment", "$12.5M", "+65% in 5 years")
            st.metric("New Artisan Businesses", "1,200+", "created since 2018")
            st.metric("Traditional Skills Preservation", "85%", "+25% vs. national average")
        
        # Case studies
        st.subheader("Community Impact Case Studies")
        
        case_col1, case_col2, case_col3 = st.columns(3)
        
        with case_col1:
            st.markdown("### Raghurajpur Artists' Village")
            st.image("https://curlytales.com/wp-content/uploads/2023/11/Pattachitra.jpg?height=150&width=250", caption="Pattachitra Artists")
            st.markdown("""
            This heritage crafts village in Odisha has transformed through responsible tourism, with 95% of families now earning through traditional Pattachitra art.
            
            **Key Success Factors**:
            - Direct sales to tourists
            - Workshops and demonstrations
            - Community management of tourism
            """)
        
        with case_col2:
            st.markdown("### Spiti Valley Homestays")
            st.image("https://discoverwithdheeraj.com/wp-content/uploads/2018/12/Spiti-Valley-Homestays.jpg?height=150&width=250", caption="Spiti Valley")
            st.markdown("""
            Local families in this remote Himalayan region host tourists in traditional homes, sharing authentic cultural experiences while generating sustainable income.
            
            **Key Success Factors**:
            - Preservation of traditional architecture
            - Revival of local cuisine
            - Cultural exchange opportunities
            """)
            
        with case_col3:
            st.markdown("### Kutch Artisan Collective")
            st.image("https://kutchcraftcollective.com/wp-content/uploads/2021/01/dedicated-craftmanship-600x400.jpg?height=150&width=250", caption="Kutch Embroidery")
            st.markdown("""
            Women artisans in Gujarat have formed cooperatives to sell directly to cultural tourists, eliminating middlemen and preserving traditional embroidery techniques.
            
            **Key Success Factors**:
            - Fair trade practices
            - Skills training for youth
            - Documentation of traditional designs
            """)
    
    # --- Responsible Tourism Pledge Tab ---
    with tab4:
        st.header("Responsible Tourism Pledge")
        st.markdown("""
        Take the CulturalCanvas Responsible Tourism Pledge to commit to practices that 
        support cultural preservation and community benefits during your travels.
        """)
        st.subheader("I Pledge To:")
        pledge_items = [
            "Respect cultural norms and traditions during my visits",
            "Support local artisans by purchasing authentic crafts directly from creators",
            "Seek permission before photographing people or cultural ceremonies",
            "Learn about the cultural context of sites and traditions I experience",
            "Choose community-based accommodations where possible",
            "Minimize my environmental impact during cultural tourism",
            "Share authentic stories that honor cultural heritage",
            "Visit lesser-known cultural sites to reduce overtourism",
            "Engage with local guides to deepen my understanding",
            "Advocate for responsible cultural tourism practices"
        ]
        for item in pledge_items:
            st.checkbox(item)
        st.subheader("Your Information")
        pledge_col1, pledge_col2 = st.columns(2)
        with pledge_col1:
            st.text_input("Name")
            st.text_input("Email")
            st.selectbox("Country", ["Select Your Country", "India", "United States", "United Kingdom", "Canada", "Australia", "Other"])
        with pledge_col2:
            st.text_area("Why responsible cultural tourism matters to you:")
            st.file_uploader("Upload a photo from your cultural travels (optional)", type=["jpg", "png"])
        if st.button("Take the Pledge"):
            st.success("Thank you for taking the Responsible Tourism Pledge! Together we can ensure that cultural tourism benefits both visitors and communities.")
            st.markdown("""
            ### What Happens Next
            - You'll receive a certificate of your pledge
            - We'll send you a responsible tourism guide
            - You'll join our community of responsible cultural travelers
            - You'll receive updates on sustainable tourism initiatives
            """)
            st.image("https://placeholder.svg?height=300&width=600", caption="Sample Responsible Tourism Pledge Certificate")
    
    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align:center; color:#64748b;'>Developed by <b>Offbeats</b> | © 2025 Vividha </div>", unsafe_allow_html=True)

if __name__ == "__main__":
    run()
