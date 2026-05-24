# SaaS-Product-Funnel-Cohort-Retention-Analysis-Python
Python analysis of a PLG SaaS funnel measuring conversion rates by acquisition channel and cohort retention at 30, 60, and 90 days.

What This Project Does
Analyzes a simulated product-led growth (PLG) funnel with 5,000 users across 6 months. Calculates conversion rates at each funnel stage, compares performance by acquisition channel, and builds a cohort retention heatmap.
Business Questions Answered
What percentage of visitors convert to paid customers?
Which acquisition channel has the highest paid conversion rate?
How does retention hold up at 30, 60, and 90 days for each monthly cohort?
How to Run
```bash
pip install pandas numpy matplotlib seaborn
python saas_funnel_analysis.py
```
Outputs appear in the `outputs/` folder.
Sample Results
Overall visitor-to-paid conversion: ~10%
Best performing channel: Referral (highest paid conversion rate)
Weakest channel: Paid Social
Cohort retention varies by channel with Referral users retaining longest
Files
File	Description
`saas_funnel_analysis.py`	Main analysis script (fully commented)
`outputs/01_funnel_overall.png`	Funnel waterfall chart
`outputs/02_conversion_by_channel.png`	Channel comparison bar chart
`outputs/03_cohort_retention_heatmap.png`	Cohort retention heatmap
`outputs/user_funnel_data.csv`	Raw user-level dataset
`outputs/channel_summary.csv`	Aggregated channel metrics
`outputs/cohort_retention.csv`	Cohort retention table
Skills Demonstrated
Funnel analysis and drop-off identification
Cohort segmentation and retention tracking
Acquisition channel performance comparison
Data visualization with matplotlib and seaborn
pandas data manipulation and aggregation
