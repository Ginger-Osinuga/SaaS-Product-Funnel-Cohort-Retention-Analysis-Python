📈 SaaS Product Funnel & Cohort Retention Analysis (Python)
Project Overview
A Python-based analysis of a simulated product-led growth (PLG) SaaS funnel tracking 5,000 users across 6 months. This project measures conversion rates at every stage of the funnel — from site visit through paid conversion — and builds a cohort retention model to track how well the product retains users at 30, 60, and 90 days after activation.
---
Business Questions Answered
What percentage of visitors convert to paid customers?
Which acquisition channel has the highest paid conversion rate?
How does retention hold up at 30, 60, and 90 days for each monthly cohort?

❓ Business Questions Answered
What percentage of visitors convert to paid customers?
Which acquisition channel has the highest paid conversion rate?
How does retention hold up at 30, 60, and 90 days for each monthly cohort?

📊 Key Analytical Insights
1. Referral Is the Highest-Quality Acquisition Channel
Referral users converted to paid customers at nearly 3x the rate of Paid Social users, despite representing a smaller share of total traffic.
The Evidence: Referral achieved the highest paid conversion rate of all five channels analyzed, while Paid Social — despite higher volume — had the lowest ROI per user acquired.
Takeaway: Not all traffic is created equal. Optimizing for referral channel growth would have a disproportionate impact on revenue relative to spend.
2. The Steepest Retention Drop Happens Between Day 30 and Day 60
Cohort retention analysis revealed that the most significant user drop-off does not happen immediately after signup — it happens in the second month.
The Evidence: Email Campaign cohorts retained meaningfully better than Direct traffic cohorts at every stage, suggesting that early lifecycle communication significantly extends user lifespan.
Takeaway: The 30-to-60-day window is the highest-priority intervention zone for retention efforts. Users who make it to Day 60 show dramatically stronger long-term retention curves.
---
🔍 Methodology
Data Generation & Technical Implementation
All data in this project is synthetically generated to simulate realistic PLG funnel behavior. The following analytical methods were applied:
Funnel Construction: Built a staged conversion funnel (Visited > Signed Up > Activated > Converted Paid) with channel-specific conversion probabilities modeled after real-world PLG benchmarks.
Channel Segmentation: Grouped users by acquisition channel (Organic Search, Paid Social, Email Campaign, Referral, Direct) and calculated paid conversion rates with an average benchmark line for comparison.
Cohort Retention Modeling: Segmented activated users into monthly signup cohorts and simulated retention decay using an exponential distribution calibrated to channel engagement levels.
Heatmap Visualization: Built a seaborn heatmap to surface retention patterns across cohorts and time periods at a glance, using color intensity to highlight high and low-retention segments.

---
📁 Files
File	Description
`saas_funnel_analysis.py`	Full analysis script with inline comments
`outputs/01_funnel_overall.png`	Funnel waterfall chart with conversion rates
`outputs/02_conversion_by_channel.png`	Paid conversion rate by acquisition channel
`outputs/03_cohort_retention_heatmap.png`	Cohort retention heatmap (Day 30 / 60 / 90)
`outputs/user_funnel_data.csv`	Raw user-level dataset
`outputs/channel_summary.csv`	Aggregated channel performance metrics
`outputs/cohort_retention.csv`	Cohort retention rates by month
---
🛠️ Tools & Libraries
Tool	Purpose
Python	Core programming language
pandas	Data manipulation and aggregation
numpy	Random data generation and numerical operations
matplotlib	Funnel and bar chart visualizations
seaborn	Cohort retention heatmap
---
📖 Glossary of Metrics
PLG (Product-Led Growth): A go-to-market strategy where the product itself drives user acquisition, conversion, and expansion rather than a traditional sales team.
Activation Rate: The percentage of signed-up users who complete a meaningful action that indicates they have experienced the product's core value.
Paid Conversion Rate: The percentage of all visitors who ultimately become paying customers.
Cohort Retention: Tracking what percentage of a defined group of users (grouped by signup month) are still active at a given point in time.
DAY 30 / 60 / 90 Retention: The percentage of activated users still active 30, 60, or 90 days after their activation date.
---
Data Source
All data is synthetically generated using Python's `numpy` and `random` libraries to simulate realistic SaaS funnel behavior.

