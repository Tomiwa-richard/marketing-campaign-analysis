# Marketing Campaign Analysis

A customer analytics case study exploring purchasing behavior, customer value, product and channel preferences, and marketing campaign response. The analysis is presented in a Jupyter notebook, with its case study and key charts included in this repository.

## Project structure

```text
.
├── README.md
├── case_study/
│   └── Marketing_Campaign_Case_Study.pdf
├── notebook/
│   └── Marketing_campaign_analysis.ipynb
├── images/
│   ├── campaign_acceptance.png
│   ├── product_spend.png
│   └── purchase_channels.png
├── requirements.txt
└── .gitignore
```

## Headline findings

- **2,212 customers** in the case study's final analysis sample.
- Income and customer spend have a strong positive correlation (**0.79**).
- **Wine** leads average spend per customer (**$305**), followed by meat (**$167**).
- Customers make the most purchases in **stores (5.81)**, followed by web (**4.09**), on average.
- The **last campaign** has the highest reported acceptance rate (**15.05%**); Campaign 2 is lowest (**1.36%**).
- The case study reports average spend of **$1,104** for customers without children at home versus **$408** for customers with children.

## Key charts

These charts are taken from the analysis notebook.

### Average spend by product category

![Average spend by product category](images/product_spend.png)

### Average purchases by channel

![Average purchases by channel](images/purchase_channels.png)

### Campaign acceptance rates

![Campaign acceptance rates](images/campaign_acceptance.png)

## Run the analysis notebook

Install the dependencies listed in `requirements.txt`, then open `notebook/Marketing_campaign_analysis.ipynb` in Jupyter. The notebook expects the source workbook at `data/marketing_campaign.xlsx`; that workbook was not included with the supplied notebook and case study, and local `data/` files are excluded from Git.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```
