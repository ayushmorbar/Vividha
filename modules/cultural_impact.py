# Cultural Impact Analysis Module
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys

sys.path.append('../utils')
from utils.dataloader import load_cultural_data

# Remove duplicate data loading and page config (should be in app.py)
def run():
    # Load cultural data
    if 'cultural_data' not in st.session_state or st.session_state.cultural_data is None:
        st.session_state.cultural_data = load_cultural_data()

    st.title("Cultural Impact Analysis")
    st.markdown("""
    Data-driven insights on the relationship between tourism and cultural preservation.
    Explore how tourism affects local communities, cultural practices, and heritage conservation.
    """)
    
    # Data source selector
    st.sidebar.markdown('---')
    st.sidebar.write('**Data Source:**')
    data_source = st.sidebar.radio('Choose data source:', ['Local CSV', 'Snowflake (Cloud)'],
                                   index=0, key='impact_data_source',
                                   help='Snowflake is not implemented in this demo. Only Local CSV is available.')
    use_snowflake = False  # Always use CSV, Snowflake not implemented
    
    # Key metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    with metrics_col1:
        st.metric(
            "Cultural Preservation Index", 
            "73/100", 
            "+5 since 2018",
            help="Composite metric measuring the preservation status of cultural heritage across India"
        )
    with metrics_col2:
        st.metric(
            "Cultural Tourism Revenue", 
            "$1.8B", 
            "+12% annually",
            help="Annual revenue generated from cultural tourism activities"
        )
    with metrics_col3:
        st.metric(
            "Artisan Livelihoods", 
            "1.2M", 
            "+3.5% annually",
            help="Number of artisans supported through cultural tourism"
        )
    with metrics_col4:
        st.metric(
            "Heritage Revitalization Projects", 
            "215", 
            "+45 since 2018",
            help="Number of active projects focused on revitalizing cultural heritage"
        )
    # Impact analysis sections
    tab1, tab2, tab3 = st.tabs([
        "Tourism & Preservation Correlation", 
        "Economic Impact", 
        "Cultural Evolution Analysis"
    ])
    
    with tab1:
        st.subheader("Tourism & Cultural Preservation Correlation")
        
        st.markdown("""
        This analysis explores the relationship between tourism levels and cultural preservation
        across different regions and art forms in India.
        """)
        
        # Filter options
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            region_filter = st.multiselect(
                "Region",
                ["North India", "South India", "East India", "West India", "Central India", "Northeast India"],
                default=["North India", "South India", "East India", "West India"]
            )
            
        with filter_col2:
            cultural_filter = st.multiselect(
                "Cultural Category",
                ["Traditional Art", "Performing Arts", "Handicrafts", "Architecture", "Festivals", "Culinary Traditions"],
                default=["Traditional Art", "Handicrafts", "Architecture"]
            )
        
        # Generate sample data
        np.random.seed(42)
        
        sample_data = []
        regions = ["North India", "South India", "East India", "West India", "Central India", "Northeast India"]
        categories = ["Traditional Art", "Performing Arts", "Handicrafts", "Architecture", "Festivals", "Culinary Traditions"]
        
        for region in regions:
            for category in categories:
                tourism_level = np.random.randint(30, 95)
                preservation_score = min(100, int(tourism_level * (0.8 + np.random.random() * 0.4)))
                community_benefit = min(100, int(tourism_level * (0.7 + np.random.random() * 0.5)))
                authenticity_impact = max(30, 100 - int(tourism_level * (0.3 + np.random.random() * 0.4)))
                
                sample_data.append({
                    "Region": region,
                    "Category": category,
                    "Tourism Level": tourism_level,
                    "Preservation Score": preservation_score,
                    "Community Benefit": community_benefit,
                    "Authenticity Impact": authenticity_impact
                })
        
        df = pd.DataFrame(sample_data)
        
        # Apply filters
        if region_filter:
            df = df[df["Region"].isin(region_filter)]
            
        if cultural_filter:
            df = df[df["Category"].isin(cultural_filter)]
        
        # Create scatter plot
        fig = px.scatter(
            df,
            x="Tourism Level",
            y="Preservation Score",
            size="Community Benefit",
            color="Region",
            hover_name="Category",
            size_max=20,
            opacity=0.7,
            title="Correlation between Tourism Level and Cultural Preservation",
            labels={
                "Tourism Level": "Tourism Level (0-100)",
                "Preservation Score": "Cultural Preservation Score (0-100)"
            },
            height=500
        )
        
        # Add trend line
        fig.add_trace(
            go.Scatter(
                x=[30, 95],
                y=[30 * 0.8, 95 * 0.8],
                mode="lines",
                name="Average Trend",
                line=dict(dash="dash", color="gray")
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation analysis
        st.markdown("### Key Insights from Correlation Analysis")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown("""
            - **Positive Correlation**: Overall, higher tourism levels correlate with better preservation scores for most cultural categories
            - **Regional Variations**: Northeast India shows the strongest positive correlation, while North India shows more mixed results
            - **Category Differences**: Traditional Arts and Handicrafts benefit most from tourism, while Performing Arts show more varied outcomes
            - **Optimal Tourism Level**: Cultural preservation benefits peak at tourism levels between 65-80, with diminishing returns beyond that
            """)
        
        with insight_col2:
            # Create correlation heatmap
            corr_data = {
                'Region': regions,
                'Tourism-Preservation Correlation': [0.78, 0.85, 0.72, 0.65, 0.80, 0.92],
                'Tourism-Authenticity Correlation': [-0.45, -0.30, -0.55, -0.60, -0.40, -0.25],
                'Tourism-Community Benefit Correlation': [0.82, 0.75, 0.70, 0.65, 0.85, 0.90]
            }
            
            corr_df = pd.DataFrame(corr_data).set_index('Region')
            
            fig = px.imshow(
                corr_df,
                text_auto=True,
                color_continuous_scale="RdBu_r",
                title="Regional Correlation Analysis",
                color_continuous_midpoint=0
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Case studies
        st.markdown("### Case Studies: Tourism & Preservation Balance")
        
        case_col1, case_col2, case_col3 = st.columns(3)
        
        with case_col1:
            st.markdown("#### Positive Example: Raghurajpur Heritage Village")
            st.image("https://placeholder.svg?height=150&width=250", caption="Pattachitra Art Village")
            st.markdown("""
            **Tourism Level**: 72/100
            **Preservation Score**: 85/100
            
            Managed tourism has led to increased investment in preserving traditional Pattachitra art and architecture, with strict quality controls and community-led initiatives.
            """)
        
        with case_col2:
            st.markdown("#### Balanced Example: Kutch Handicrafts")
            st.image("https://placeholder.svg?height=150&width=250", caption="Kutch Embroidery")
            st.markdown("""
            **Tourism Level**: 65/100
            **Preservation Score**: 75/100
            
            Tourism has supported traditional embroidery practices while maintaining authenticity through artisan cooperatives and documentation efforts.
            """)
            
        with case_col3:
            st.markdown("#### Negative Example: Jaipur Block Printing")
            st.image("https://placeholder.svg?height=150&width=250", caption="Block Printing")
            st.markdown("""
            **Tourism Level**: 88/100
            **Preservation Score**: 60/100
            
            High tourism demand has led to mass production, quality compromise, and reduced authentic practices in some areas, though preservation efforts are improving.
            """)
    
    with tab2:
        st.subheader("Economic Impact Analysis")
        
        st.markdown("""
        Explore how cultural tourism contributes to economic development and the distribution
        of benefits across different stakeholders.
        """)
        
        # Economic impact metrics
        impact_col1, impact_col2 = st.columns(2)
        
        with impact_col1:
            # Create treemap of economic benefit distribution
            economic_data = {
                'Sector': ['Artisans & Craftspeople', 'Artisans & Craftspeople', 'Hospitality & Accommodations', 
                           'Hospitality & Accommodations', 'Local Businesses', 'Local Businesses', 
                           'Transportation', 'Cultural Institutions', 'Guides & Interpreters', 'Tour Operators', 
                           'Government Revenue'],
                'Subsector': ['Direct Sales', 'Workshops & Training', 'Hotels', 'Homestays', 
                             'Restaurants', 'Retail', 'Local Transport', 'Museums & Sites', 
                             'Local Guides', 'Package Tours', 'Taxes & Fees'],
                'Value': [250, 80, 320, 90, 180, 120, 150, 110, 80, 200, 160]
            }
            
            eco_df = pd.DataFrame(economic_data)
            
            fig = px.treemap(
                eco_df,
                path=['Sector', 'Subsector'],
                values='Value',
                title="Distribution of Cultural Tourism Revenue (Millions USD)",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with impact_col2:
            st.markdown("### Key Economic Findings")
            
            st.markdown("""
            - **Revenue Distribution**: Artisans and local businesses receive approximately 35% of total cultural tourism revenue
            - **Job Creation**: Cultural tourism supports approximately 1.2 million direct and 3.5 million indirect jobs
            - **Multiplier Effect**: Each $1 spent on cultural tourism generates an additional $2.3 in the local economy
            - **Seasonal Variations**: Revenue fluctuates by 40-65% between peak and off-peak seasons
            - **Regional Disparities**: Economic benefits vary significantly by region, with established tourism circuits capturing 70% of revenue
            """)
            
            # Create chart of economic impact by stakeholder
            stakeholder_impact = {
                'Stakeholder': ['Artisans', 'Local Communities', 'Tourism Businesses', 'Cultural Institutions', 'Government'],
                'Direct Revenue (%)': [15, 25, 35, 10, 15],
                'Indirect Benefits (%)': [25, 30, 20, 15, 10]
            }
            
            stakeholder_df = pd.DataFrame(stakeholder_impact)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=stakeholder_df['Stakeholder'],
                y=stakeholder_df['Direct Revenue (%)'],
                name='Direct Revenue',
                marker_color='blue'
            ))
            
            fig.add_trace(go.Bar(
                x=stakeholder_df['Stakeholder'],
                y=stakeholder_df['Indirect Benefits (%)'],
                name='Indirect Benefits',
                marker_color='green'
            ))
            
            fig.update_layout(
                title="Economic Benefits by Stakeholder Group",
                barmode='group',
                xaxis_title="Stakeholder Group",
                yaxis_title="Percentage of Total Benefits"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Longitudinal economic analysis
        st.subheader("Longitudinal Economic Impact")
        
        # Generate sample data for economic trends
        years = list(range(2015, 2024))
        total_revenue = [850, 920, 1050, 1180, 1310, 980, 1100, 1450, 1740]  # in millions USD
        artisan_income = [12500, 13200, 14100, 15300, 16500, 13800, 15000, 18500, 22000]  # annual average in INR
        cultural_investment = [45, 52, 60, 68, 75, 55, 65, 85, 105]  # in millions USD
        
        # Create multi-line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years,
            y=total_revenue,
            name="Total Cultural Tourism Revenue (M USD)",
            line=dict(color='blue', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=cultural_investment,
            name="Cultural Heritage Investment (M USD)",
            line=dict(color='green', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=[rev * 0.15 for rev in total_revenue],
            name="Artisan Direct Revenue (M USD)",
            line=dict(color='orange', width=3)
        ))
        
        fig.update_layout(
            title="Economic Impact Trends (2015-2023)",
            xaxis_title="Year",
            yaxis_title="Value (Millions USD)",
            legend=dict(x=0.01, y=0.99),
            height=500
        )
        
        # Add COVID-19 impact annotation
        fig.add_annotation(
            x=2020,
            y=980,
            text="COVID-19 Impact",
            showarrow=True,
            arrowhead=1
        )
        
        # Add recovery annotation
        fig.add_annotation(
            x=2022,
            y=1450,
            text="Post-COVID Recovery",
            showarrow=True,
            arrowhead=1
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Sustainable economic development
        st.subheader("Sustainable Economic Development")
        
        sus_col1, sus_col2, sus_col3 = st.columns(3)
        
        with sus_col1:
            st.markdown("### Artisan Cooperatives")
            st.image("https://placeholder.svg?height=150&width=250", caption="Artisan Cooperative")
            st.markdown("""
            **Economic Impact**: Artisan cooperatives have increased average income by 35% through direct sales and eliminating middlemen.
            
            **Sustainability Factor**: 85/100
            
            Over 300 cooperatives now support more than 25,000 artisan families across India.
            """)
        
        with sus_col2:
            st.markdown("### Cultural Tourism Corridors")
            st.image("https://placeholder.svg?height=150&width=250", caption="Tourism Corridor")
            st.markdown("""
            **Economic Impact**: Integrated tourism corridors connecting multiple cultural sites have increased visitor stay duration by 45%.
            
            **Sustainability Factor**: 75/100
            
            12 major cultural corridors have been developed, distributing tourism benefits across 85+ communities.
            """)
            
        with sus_col3:
            st.markdown("### Digital Marketplaces")
            st.image("https://placeholder.svg?height=150&width=250", caption="Online Marketplace")
            st.markdown("""
            **Economic Impact**: Online platforms have created year-round revenue streams, reducing seasonal fluctuations by 30%.
            
            **Sustainability Factor**: 80/100
            
            Digital sales now account for 25% of total artisan revenue, with 55% coming from international customers.
            """)
    
    with tab3:
        st.subheader("Cultural Evolution Analysis")
        
        st.markdown("""
        This analysis examines how traditional cultural practices are evolving in response to
        tourism, globalization, and changing social contexts.
        """)
        
        # Evolution metrics
        evolution_col1, evolution_col2 = st.columns(2)
        
        with evolution_col1:
            # Create chart for practice adoption among younger generations
            age_groups = ['Under 20', '20-35', '35-50', '50-65', 'Over 65']
            traditional_participation = [30, 45, 65, 85, 95]
            modified_participation = [75, 65, 45, 30, 15]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=age_groups,
                y=traditional_participation,
                name='Traditional Practice Participation',
                marker_color='orange'
            ))
            
            fig.add_trace(go.Bar(
                x=age_groups,
                y=modified_participation,
                name='Modified Practice Participation',
                marker_color='blue'
            ))
            
            fig.update_layout(
                title="Cultural Practice Participation by Age Group",
                barmode='group',
                xaxis_title="Age Group",
                yaxis_title="Participation Rate (%)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with evolution_col2:
            st.markdown("### Key Evolution Patterns")
            
            st.markdown("""
            1. **Generational Adaptation**: Younger generations are more likely to practice modified versions of traditional arts
            
            2. **Material Evolution**: 65% of traditional art forms now incorporate some modern materials while maintaining traditional techniques
            
            3. **Thematic Changes**: Contemporary social themes now appear in 40% of traditional art forms
            
            4. **Technical Modifications**: Production processes have been modified in 55% of cases to meet tourism demand while maintaining quality
            
            5. **Digital Integration**: 35% of traditional cultural practices now have significant digital components for documentation or creation
            """)
            
            # Create gauge chart for innovation vs tradition balance
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=63,
                title={'text': "Innovation vs Tradition Balance"},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "red"},
                        {'range': [40, 60], 'color': "yellow"},
                        {'range': [60, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': 63
                    }
                }
            ))
            
            fig.update_layout(
                height=300,
                annotations=[{
                    'x': 0.5,
                    'y': 0.3,
                    'text': "Tradition « Balance » Innovation",
                    'showarrow': False
                }]
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Evolution case studies
        st.subheader("Cultural Evolution Case Studies")
        
        tabs = st.tabs(["Traditional Art", "Performing Arts", "Crafts & Textiles"])
        
        with tabs[0]:
            st.markdown("### Evolution of Traditional Art Forms")
            
            art_col1, art_col2 = st.columns(2)
            
            with art_col1:
                st.image("https://placeholder.svg?height=300&width=400", caption="Traditional vs Contemporary Madhubani")
                
                st.markdown("""
                #### Madhubani Painting Evolution
                
                **Traditional Practice**: Natural pigments, religious themes, ritual purposes
                
                **Contemporary Adaptations**:
                - Use of acrylic colors alongside natural pigments
                - Expansion to social and environmental themes
                - Adaptation to canvas, paper, and commercial products
                - Digital documentation and online teaching
                
                **Preservation Status**: Strong core traditions with conscious innovation
                """)
            
            with art_col2:
                # Create evolution timeline
                timeline_data = {
                    "Stage": ["Pre-Tourism", "Early Tourism", "Commercialization", "Digital Age", "Balanced Revival"],
                    "Period": ["Before 1970s", "1970s-1980s", "1990s-2000s", "2010-2015", "2015-Present"],
                    "Authenticity": [95, 85, 60, 50, 75],
                    "Economic Viability": [30, 45, 75, 65, 85],
                    "Practice Prevalence": [45, 55, 70, 60, 80]
                }
                
                timeline_df = pd.DataFrame(timeline_data)
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=timeline_df["Period"],
                    y=timeline_df["Authenticity"],
                    name="Authenticity Score",
                    line=dict(color='red', width=3)
                ))
                
                fig.add_trace(go.Scatter(
                    x=timeline_df["Period"],
                    y=timeline_df["Economic Viability"],
                    name="Economic Viability",
                    line=dict(color='green', width=3)
                ))
                
                fig.add_trace(go.Scatter(
                    x=timeline_df["Period"],
                    y=timeline_df["Practice Prevalence"],
                    name="Practice Prevalence",
                    line=dict(color='blue', width=3)
                ))
                
                fig.update_layout(
                    title="Evolution Timeline of Traditional Art",
                    xaxis_title="Time Period",
                    yaxis_title="Score (0-100)",
                    legend=dict(x=0.01, y=0.99)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                #### Key Insight
                
                After a period of commercialization that threatened authenticity, there has been a conscious revival movement focusing on balancing tradition with innovation, resulting in both improved economic viability and authenticity.
                """)
        
        with tabs[1]:
            st.markdown("### Evolution of Performing Arts")
            
            dance_col1, dance_col2 = st.columns(2)
            
            with dance_col1:
                st.image("https://placeholder.svg?height=300&width=400", caption="Bharatanatyam Evolution")
                
                st.markdown("""
                #### Bharatanatyam Evolution
                
                **Traditional Practice**: Temple performances, religious themes, lengthy presentations
                
                **Contemporary Adaptations**:
                - Shorter, tourism-friendly performances
                - Incorporation of contemporary themes
                - Fusion with other dance forms
                - Adaptations for international audiences
                - Digital performances and teaching
                
                **Preservation Status**: Core techniques preserved with presentation adaptations
                """)
            
            with dance_col2:
                # Create adaptation heatmap
                adaptation_data = {
                    'Element': ['Performance Duration', 'Religious Content', 'Costume Elements', 'Musical Accompaniment', 'Venue', 'Narrative Structure'],
                    'Tourism Adaptation': [80, 65, 40, 55, 85, 70],
                    'Cultural Preservation': [50, 75, 85, 80, 60, 75]
                }
                
                adapt_df = pd.DataFrame(adaptation_data)
                
                fig = px.scatter(
                    adapt_df,
                    x="Tourism Adaptation",
                    y="Cultural Preservation",
                    text="Element",
                    size=[60] * len(adapt_df),
                    color="Tourism Adaptation",
                    color_continuous_scale="Viridis",
                    labels={
                        "Tourism Adaptation": "Degree of Adaptation for Tourism (0-100)",
                        "Cultural Preservation": "Level of Cultural Preservation (0-100)"
                    },
                    title="Balance of Tourism Adaptation and Cultural Preservation"
                )
                
                fig.update_traces(textposition='top center')
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                #### Key Insight
                
                Elements like performance duration and venue have been significantly adapted for tourism, while core elements like costumes and musical structure remain more closely tied to tradition. This strategic adaptation has allowed the art form to remain economically viable while preserving its cultural essence.
                """)
        
        with tabs[2]:
            st.markdown("### Evolution of Crafts & Textiles")
            
            craft_col1, craft_col2 = st.columns(2)
            
            with craft_col1:
                st.image("https://placeholder.svg?height=300&width=400", caption="Textile Evolution")
                
                st.markdown("""
                #### Textile Craft Evolution
                
                **Traditional Practice**: Hand-spun materials, natural dyes, traditional motifs, local use
                
                **Contemporary Adaptations**:
                - Incorporation of commercial materials
                - Mix of natural and chemical dyes
                - Simplified motifs for mass production
                - New product applications (fashion, home decor)
                - Global market adaptation
                
                **Preservation Status**: Variable, with some regions maintaining stronger traditions
                """)
            
            with craft_col2:
                # Create evolution quadrant chart
                evolution_data = {
                    'Craft': ['Banaras Brocade', 'Pochampally Ikat', 'Kanchipuram Silk', 'Bagru Block Print', 
                              'Kutch Embroidery', 'Chanderi Weaving', 'Pashmina Shawls', 'Kalamkari'],
                    'Traditional Technique Preservation': [85, 75, 90, 65, 80, 70, 60, 85],
                    'Commercial Adaptation': [80, 65, 75, 90, 60, 85, 95, 70],
                    'Market Success': [85, 70, 80, 75, 65, 75, 90, 60]
                }
                
                evo_df = pd.DataFrame(evolution_data)
                
                fig = px.scatter(
                    evo_df,
                    x="Commercial Adaptation",
                    y="Traditional Technique Preservation",
                    size="Market Success",
                    color="Market Success",
                    hover_name="Craft",
                    text="Craft",
                    size_max=20,
                    color_continuous_scale="Viridis",
                    labels={
                        "Commercial Adaptation": "Degree of Commercial Adaptation (0-100)",
                        "Traditional Technique Preservation": "Preservation of Traditional Techniques (0-100)"
                    },
                    title="Craft Evolution Quadrant Analysis"
                )
                
                # Add quadrant lines
                fig.add_shape(
                    type="line", line=dict(dash="dash", color="gray"),
                    x0=75, y0=0, x1=75, y1=100
                )
                
                fig.add_shape(
                    type="line", line=dict(dash="dash", color="gray"),
                    x0=0, y0=75, x1=100, y1=75
                )
                
                # Add quadrant labels
                fig.add_annotation(x=87, y=87, text="Balanced Success", showarrow=False)
                fig.add_annotation(x=87, y=37, text="Over-Commercialized", showarrow=False)
                fig.add_annotation(x=37, y=87, text="Traditional but Limited", showarrow=False)
                fig.add_annotation(x=37, y=37, text="At Risk", showarrow=False)
                
                fig.update_traces(textposition='top center')
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                #### Key Insight
                
                Crafts that have achieved the best balance between commercial adaptation and traditional preservation (upper right quadrant) tend to be the most successful in the market. This demonstrates that cultural preservation and economic success can be complementary with the right approach.
                """)
        
        # Future trends and recommendations
        st.subheader("Future Trends & Recommendations")
        
        future_col1, future_col2 = st.columns(2)
        
        with future_col1:
            st.markdown("### Projected Cultural Evolution Trends")
            
            st.markdown("""
            1. **Digital Documentation**: Increased use of technology to document and preserve traditional knowledge
            
            2. **Sustainable Adaptation**: Growing focus on environmentally sustainable materials and practices
            
            3. **Cross-Cultural Fusion**: More deliberate fusion of traditional techniques with global influences
            
            4. **Community Ownership**: Strengthened intellectual property protections for traditional cultural expressions
            
            5. **Educational Integration**: Formal inclusion of traditional arts in educational curricula
            
            6. **Experience Economy**: Shift from product-focused to experience-focused cultural tourism
            """)
        
        with future_col2:
            st.markdown("### Recommendations for Balanced Evolution")
            
            st.markdown("""
            1. **Cultural Documentation**: Invest in comprehensive documentation of traditional practices
            
            2. **Apprenticeship Programs**: Support master-apprentice relationships with stipends and recognition
            
            3. **Adaptive Authenticity**: Develop frameworks for evaluating appropriate innovation vs. harmful modification
            
            4. **Community Control**: Ensure communities maintain decision-making authority over cultural adaptations
            
            5. **Market Education**: Educate consumers about the value of authentic cultural products
            
            6. **Sustainable Tourism**: Implement carrying capacity limits at cultural sites to prevent over-commercialization
            """)
    
    # Call to action
    st.header("Get Involved in Cultural Preservation")
    
    st.markdown("""
    Your involvement in responsible cultural tourism can make a significant difference in preserving India's rich heritage.
    Here are ways you can contribute:
    """)
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        st.markdown("### As a Tourist")
        
        st.markdown("""
        - Choose community-based cultural experiences
        - Purchase directly from artisans
        - Learn about the cultural context before visiting
        - Respect photography guidelines and privacy
        - Share authentic stories that honor traditions
        """)
    
    with action_col2:
        st.markdown("### As a Professional")
        
        st.markdown("""
        - Partner with cultural preservation organizations
        - Implement sustainable tourism practices
        - Invest in artisan communities
        - Document and promote authentic cultural experiences
        - Provide training opportunities for local guides
        """)
            
    with action_col3:
        st.markdown("### As a Policymaker")
        
        st.markdown("""
        - Create incentives for cultural preservation
        - Develop sustainable tourism frameworks
        - Support documentation and education initiatives
        - Protect intellectual property of traditional knowledge
        - Invest in community-based tourism infrastructure
        """)
    

    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align:center; color:#64748b;'>Developed by <b>Offbeats</b> | © 2025 Vividha </div>", unsafe_allow_html=True)
