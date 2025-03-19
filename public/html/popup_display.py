from datatypes.KeywordRankingRuleByScrappingDatatypes import RankingKeyword, FinalRankAnalysis


def popup_display(row: FinalRankAnalysis):

    keys = [
        f"""
    <div style="
        padding: 8px;
        border-bottom: 1px solid #eee;
        font-family: Arial, sans-serif;
        color: #212529;
    ">
        <strong style="font-size: 14px; color: #007bff;">{d.keyword}</strong>
        <div style="margin-top: 4px; font-size: 12px; color: #6c757d;">
            Percentage: <span style="color: #28a745; font-weight: bold;">{d.percentage}%</span><br>
            Position: <span style="color: #ffc107; font-weight: bold;">{d.location_rank.rank}</span><br>
            Against all businesses: <span style="color: #dc3545; font-weight: bold;">{d.location_rank.percentage}%</span>
        </div>
    </div>
    """
        for d in row.data
    ]


# Complete Popup Design
    return f"""
    <div style="
        font-family: Arial, sans-serif;
        background-color: #fff;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #ddd;
        max-width: 280px;
    ">
        <h2 style="
            margin-top: 0;
            font-size: 16px;
            color: #212529;
            border-bottom: 2px solid #007bff;
            padding-bottom: 4px;
        ">
            Keyword Performance: <span style="color: #007bff;">{row.average_percentage}%</span>
        </h2>
        {''.join(keys)}
    </div>
    """
