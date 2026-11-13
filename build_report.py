import json

report = {
    "id": 0,
    "layoutOptimization": 0,
    "resourcePackages": [
        {
            "resourcePackage": {
                "name": "SharedResources",
                "type": 2,
                "items": [{"name": "CY24SU10", "type": 0}]
            }
        }
    ],
    "sections": []
}

page1 = {
    "id": 0,
    "name": "Executive Overview",
    "displayName": "Executive Overview",
    "filters": "[]",
    "height": 720.0,
    "width": 1280.0,
    "config": "{\"objects\":{\"background\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#0F1C2E\"}}}}]}}",
    "visualContainers": [
        {
            "x": 20, "y": 10, "z": 0, "width": 550, "height": 65,
            "config": "{\"name\":\"title1\",\"layouts\":[{\"id\":0,\"position\":{\"x\":20,\"y\":10,\"z\":0,\"width\":550,\"height\":65}}],\"singleVisual\":{\"visualType\":\"textbox\",\"objects\":{\"general\":[{\"properties\":{\"paragraphs\":[{\"textRuns\":[{\"value\":\"SUPPLY CHAIN DISRUPTION MONITORING AND LEAD TIME ESTIMATION\",\"textStyle\":{\"fontSize\":16,\"fontFamily\":\"Segoe UI Bold\",\"color\":\"#FFFFFF\"}}]}]}}]}}}"
        },
        {
            "x": 20, "y": 85, "z": 1000, "width": 235, "height": 95,
            "config": "{\"name\":\"kpi1\",\"layouts\":[{\"id\":0,\"position\":{\"x\":20,\"y\":85,\"z\":1000,\"width\":235,\"height\":95}}],\"singleVisual\":{\"visualType\":\"card\",\"projections\":{\"Values\":[{\"queryRef\":\"Supplier_Performance_Summary.Total Suppliers\"}]},\"objects\":{\"labels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#FFFFFF\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"32D\"}}}}}],\"categoryLabels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#B0B0B0\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"11D\"}}}}}],\"calloutValue\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#00D4FF\"}}}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#1A2332\"}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"color\":{\"solid\":{\"color\":\"#00D4FF\"}}}}]}}}"
        },
        {
            "x": 265, "y": 85, "z": 2000, "width": 235, "height": 95,
            "config": "{\"name\":\"kpi2\",\"layouts\":[{\"id\":0,\"position\":{\"x\":265,\"y\":85,\"z\":2000,\"width\":235,\"height\":95}}],\"singleVisual\":{\"visualType\":\"card\",\"projections\":{\"Values\":[{\"queryRef\":\"Supplier_Performance_Summary.Total Products\"}]},\"objects\":{\"labels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#FFFFFF\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"32D\"}}}}}],\"categoryLabels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#B0B0B0\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"11D\"}}}}}],\"calloutValue\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#7B68EE\"}}}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#1A2332\"}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"color\":{\"solid\":{\"color\":\"#7B68EE\"}}}}]}}}"
        },
        {
            "x": 510, "y": 85, "z": 3000, "width": 235, "height": 95,
            "config": "{\"name\":\"kpi3\",\"layouts\":[{\"id\":0,\"position\":{\"x\":510,\"y\":85,\"z\":3000,\"width\":235,\"height\":95}}],\"singleVisual\":{\"visualType\":\"card\",\"projections\":{\"Values\":[{\"queryRef\":\"Supplier_Performance_Summary.Avg Lead Time\"}]},\"objects\":{\"labels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#FFFFFF\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"32D\"}}}}}],\"categoryLabels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#B0B0B0\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"11D\"}}}}}],\"calloutValue\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#FFA500\"}}}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#1A2332\"}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"color\":{\"solid\":{\"color\":\"#FFA500\"}}}}]}}}"
        },
        {
            "x": 755, "y": 85, "z": 4000, "width": 235, "height": 95,
            "config": "{\"name\":\"kpi4\",\"layouts\":[{\"id\":0,\"position\":{\"x\":755,\"y\":85,\"z\":4000,\"width\":235,\"height\":95}}],\"singleVisual\":{\"visualType\":\"card\",\"projections\":{\"Values\":[{\"queryRef\":\"Supplier_Performance_Summary.High Risk %\"}]},\"objects\":{\"labels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#FFFFFF\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"32D\"}}}}}],\"categoryLabels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#B0B0B0\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"11D\"}}}}}],\"calloutValue\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#FF4444\"}}}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#1A2332\"}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"color\":{\"solid\":{\"color\":\"#FF4444\"}}}}]}}}"
        },
        {
            "x": 1000, "y": 85, "z": 5000, "width": 260, "height": 95,
            "config": "{\"name\":\"kpi5\",\"layouts\":[{\"id\":0,\"position\":{\"x\":1000,\"y\":85,\"z\":5000,\"width\":260,\"height\":95}}],\"singleVisual\":{\"visualType\":\"card\",\"projections\":{\"Values\":[{\"queryRef\":\"Supplier_Performance_Summary.Avg Supplier Reliability\"}]},\"objects\":{\"labels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#FFFFFF\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"32D\"}}}}}],\"categoryLabels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#B0B0B0\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"11D\"}}}}}],\"calloutValue\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#00FF88\"}}}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#1A2332\"}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"color\":{\"solid\":{\"color\":\"#00FF88\"}}}}]}}}"
        },
        {
            "x": 20, "y": 195, "z": 6000, "width": 400, "height": 250,
            "config": "{\"name\":\"donut1\",\"layouts\":[{\"id\":0,\"position\":{\"x\":20,\"y\":195,\"z\":6000,\"width\":400,\"height\":250}}],\"singleVisual\":{\"visualType\":\"donutChart\",\"projections\":{\"Category\":[{\"queryRef\":\"Supplier_Performance_Summary.risk_classification\"}],\"Y\":[{\"queryRef\":\"CountNonNull(Supplier_Performance_Summary.product_id)\"}]},\"objects\":{\"legend\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"labelColor\":{\"solid\":{\"color\":\"#FFFFFF\"}}}}],\"labels\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#FFFFFF\"}}}}],\"dataPoint\":[{\"properties\":{\"fill\":{\"solid\":{\"color\":\"#FF4444\"}}},\"selector\":{\"data\":[{\"scopeId\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}}},\"Property\":\"risk_classification\"},\"Right\":{\"Literal\":{\"Value\":\"\\\"High Risk\\\"\"}}}}]}}},{\"properties\":{\"fill\":{\"solid\":{\"color\":\"#FFA500\"}}},\"selector\":{\"data\":[{\"scopeId\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}}},\"Property\":\"risk_classification\"},\"Right\":{\"Literal\":{\"Value\":\"\\\"Moderate Risk\\\"\"}}}}]}}}]},\"vcObjects\":{\"title\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"text\":\"Risk Classification\",\"color\":{\"solid\":{\"color\":\"#FFFFFF\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"14D\"}}}}}],\"background\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#1A2332\"}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"color\":{\"solid\":{\"color\":\"#2A3F5F\"}}}}]}}}"
        },
        {
            "x": 435, "y": 195, "z": 7000, "width": 825, "height": 250,
            "config": "{\"name\":\"bar1\",\"layouts\":[{\"id\":0,\"position\":{\"x\":435,\"y\":195,\"z\":7000,\"width\":825,\"height\":250}}],\"singleVisual\":{\"visualType\":\"clusteredBarChart\",\"projections\":{\"Category\":[{\"queryRef\":\"Supplier_Performance_Summary.supplier_country\"}],\"Y\":[{\"queryRef\":\"Supplier_Performance_Summary.Avg Disruption Likelihood\"}]},\"objects\":{\"categoryAxis\":[{\"properties\":{\"labelColor\":{\"solid\":{\"color\":\"#FFFFFF\"}}}}],\"valueAxis\":[{\"properties\":{\"labelColor\":{\"solid\":{\"color\":\"#FFFFFF\"}}}}],\"dataPoint\":[{\"properties\":{\"fill\":{\"solid\":{\"color\":\"#FF6B6B\"}}}}]},\"vcObjects\":{\"title\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"text\":\"Avg Disruption Likelihood by Country\",\"color\":{\"solid\":{\"color\":\"#FFFFFF\"}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"14D\"}}}}}],\"background\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#1A2332\"}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"color\":{\"solid\":{\"color\":\"#2A3F5F\"}}}}]}}}"
        },
        {
            "x": 20, "y": 460, "z": 8000, "width": 640, "height": 245,
            "config": "{\"name\":\"table1\",\"layouts\":[{\"id\":0,\"position\":{\"x\":20,\"y\":460,\"z\":8000,\"width\":640,\"height\":245}}],\"singleVisual\":{\"visualType\":\"tableEx\",\"projections\":{\"Values\":[{\"queryRef\":\"Supplier_Performance_Summary.supplier_id\"},{\"queryRef\":\"Supplier_Performance_Summary.supplier_country\"},{\"queryRef\":\"Supplier_Performance_Summary.avg_lead_time_days\"},{\"queryRef\":\"Supplier_Performance_Summary.avg_supplier_reliability\"},{\"queryRef\":\"Supplier_Performance_Summary.avg_disruption_likelihood\"},{\"queryRef\":\"Supplier_Performance_Summary.risk_classification\"}]},\"objects\":{\"grid\":[{\"properties\":{\"gridVertical\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"gridHorizontal\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}}}}],\"columnHeaders\":[{\"properties\":{\"fontColor\":{\"solid\":{\"color\":\"#FFFFFF\"}},\"backColor\":{\"solid\":{\"color\":\"#2A3F5F\"}}}}],\"values\":[{\"properties\":{\"fontColor\":{\"solid\":{\"color\":\"#FFFFFF\"}},\"backColor\":{\"solid\":{\"color\":\"#1A2332\"}}}}]},\"vcObjects\":{\"title\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"text\":\"Supplier Risk Overview\",\"color\":{\"solid\":{\"color\":\"#FFFFFF\"}}}],\"background\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#1A2332\"}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"color\":{\"solid\":{\"color\":\"#2A3F5F\"}}}}]}}}"
        },
        {
            "x": 675, "y": 460, "z": 9000, "width": 585, "height": 245,
            "config": "{\"name\":\"scatter1\",\"layouts\":[{\"id\":0,\"position\":{\"x\":675,\"y\":460,\"z\":9000,\"width\":585,\"height\":245}}],\"singleVisual\":{\"visualType\":\"scatterChart\",\"projections\":{\"X\":[{\"queryRef\":\"Supplier_Performance_Summary.avg_supplier_reliability\"}],\"Y\":[{\"queryRef\":\"Supplier_Performance_Summary.avg_lead_time_days\"}],\"Size\":[{\"queryRef\":\"Supplier_Performance_Summary.avg_disruption_likelihood\"}]},\"objects\":{\"categoryAxis\":[{\"properties\":{\"labelColor\":{\"solid\":{\"color\":\"#FFFFFF\"}}}}],\"valueAxis\":[{\"properties\":{\"labelColor\":{\"solid\":{\"color\":\"#FFFFFF\"}}}}]},\"vcObjects\":{\"title\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"text\":\"Reliability vs Lead Time\",\"color\":{\"solid\":{\"color\":\"#FFFFFF\"}}}],\"background\":[{\"properties\":{\"color\":{\"solid\":{\"color\":\"#1A2332\"}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"color\":{\"solid\":{\"color\":\"#2A3F5F\"}}}}]}}}"
        }
    ]
}

report["sections"] = [page1]
with open(r'B:\Project\Data Science\project\Supply Chain Disruption Monitoring.Report\report.json', 'w') as f:
    json.dump(report, f, indent=2)

print("Done")
