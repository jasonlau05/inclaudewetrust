# US Investing Guidance Knowledge Base

<a id="kb-scope"></a>
## KB-SCOPE — Purpose and boundaries

This knowledge base supports general educational investing guidance for US users. It is not investment, fiduciary, brokerage, legal, tax, accounting, insurance, or credit advice.

Core principles:

- Match each dollar to its **goal, earliest use date, liquidity need, and consequence of loss**.
- Use the lower of **risk tolerance** and **risk capacity** as the practical risk ceiling.
- Establish basic financial resilience before taking substantial market risk.
- Prefer simple, diversified, low-cost portfolios over prediction, trading, or concentrated bets.
- Treat account selection, tax treatment, and investment selection as separate decisions.
- Never invent current prices, tickers, yields, returns, fund expenses, holdings, laws, or contribution limits.
- Verify all yearly limits, tax rules, plan provisions, student-loan programs, and market data before use.

Sources: [Investor.gov—Asset allocation](https://www.investor.gov/introduction-investing/getting-started/asset-allocation), [Investor.gov—Build wealth over time](https://www.investor.gov/build-wealth-over-time-through-saving-and-investing), [CFP Board—Code and Standards](https://www.cfp.net/ethics/code-of-ethics-and-standards-of-conduct).

---

<a id="profile-schema"></a>
# PROFILE-SCHEMA — User profile and missing-information questions

Store `unknown` explicitly. Do not infer a favorable answer from age, salary, occupation, clicks, or confidence. Date-stamp the profile and recheck it after major life events.

| ID | Parameter and type | Allowed values or structure | Why it changes strategy | Ask when missing |
|---|---|---|---|---|
| PS-001 | `age`: integer | Nonnegative age in years; `unknown` | Helps identify legal/minor issues and likely life stage, but does not determine allocation by itself. | “How old are you?” |
| PS-002 | `life_stage`: enum | student, early career, mid-career, pre-retirement, retired, other | Indicates likely income changes, withdrawal status, benefit choices, and competing goals. | “Are you studying, working, approaching retirement, or already retired?” |
| PS-003 | `household_status`: object | single, partnered, married, separated, divorced, widowed; whether finances are joint | Ownership, taxes, survivor needs, legal rights, and household risk capacity differ. | “Do you plan finances individually or with a spouse or partner?” |
| PS-004 | `tax_residency`: object | US citizen/resident/nonresident/unknown; state; other countries of tax residence | Account eligibility, withholding, treaties, foreign reporting, and state taxes may change the answer. | “Where are you a tax resident, and in which state do you live?” |
| PS-005 | `income`: object | annual gross income, take-home income, recurring income, variable compensation | Determines contribution capacity, tax context, and ability to absorb losses. | “What are your approximate annual income and monthly take-home pay?” |
| PS-006 | `income_stability`: enum/object | very stable, stable, variable, seasonal, commission-based, uncertain; number of earners | Unstable or correlated earnings increase liquidity needs and reduce risk capacity. | “How predictable is your income, and how would a recession or job loss affect it?” |
| PS-007 | `occupation`: object | occupation, industry, employment type, physical demands, expected career changes | Human capital may be stable, cyclical, physically vulnerable, or correlated with portfolio holdings. | “What is your occupation, industry, and employment type?” |
| PS-008 | `expected_income_changes`: object | graduation, residency completion, promotion, retirement, job change, deployment, leave, business seasonality | Expected transitions affect tax choices and near-term liquidity, but uncertain future income should not be treated as guaranteed. | “Do you expect a major income or employment change soon?” |
| PS-009 | `essential_expenses`: currency/time | Monthly essential spending and known irregular obligations | Used to size reserves and determine whether investing would endanger essentials. | “What do you need each month for housing, food, insurance, transportation, care, and minimum debt payments?” |
| PS-010 | `cash_reserves`: object | liquid amount, location, insurance status, months of essential expenses | A low reserve can turn volatility or an unexpected bill into forced selling or debt. | “How much safe, readily available cash do you have, excluding investments?” |
| PS-011 | `debts`: array | type, balance, APR, fixed/variable, minimum payment, term, delinquency, collateral | Debt cost and protections may dominate the expected benefit of investing. | “List each debt’s type, balance, interest rate, minimum payment, and whether it is current.” |
| PS-012 | `student_loans`: object | federal/private, loan types, rates, payment plan, qualifying employer, PSLF/IDR status | Extra repayment or refinancing can conflict with federal protections or forgiveness. | “Are the loans federal or private, and are PSLF or income-driven repayment relevant?” |
| PS-013 | `employer_match`: object | formula, required employee percentage, vesting, per-pay-period rule, true-up | An affordable vested match is often a high-priority benefit. | “Does your employer match retirement contributions, and what are the formula and vesting rules?” |
| PS-014 | `available_accounts`: set/object | 401(k), 403(b), governmental or nongovernmental 457(b), TSP, pension, HSA, IRA, SEP-IRA, Solo 401(k), SIMPLE IRA, 529, taxable account | Fees, tax treatment, liquidity, creditor exposure, and investment menus differ. | “Which workplace, health, retirement, education, and brokerage accounts are available?” |
| PS-015 | `plan_quality`: object | fees, expense ratios, annuity charges, surrender terms, investment menu, loans, distributions | The account label alone does not establish that the plan is low-cost or flexible. | “What investments and total fees does the plan offer?” |
| PS-016 | `tax_profile`: object | filing status, estimated taxable income, MAGI, marginal federal/state bracket, workplace-plan coverage | Drives Roth-versus-traditional analysis, deductions, phaseouts, and conversions. | “What is your filing status and approximate taxable income or marginal tax bracket?” |
| PS-017 | `current_assets`: array | cash, funds, stocks, bonds, real estate, business interests, crypto; owner, basis, account | Total allocation and liquidity cannot be judged one account at a time. | “What assets and investments do you already own, and in which accounts?” |
| PS-018 | `concentrated_exposure`: object | employer stock, RSUs, options, sector, business, property, country, currency | Career, compensation, and wealth may all fail together when exposures are correlated. | “How much of your wealth or future compensation depends on one employer, stock, sector, property, or business?” |
| PS-019 | `pension_and_income_floor`: object | vesting, formula, COLA, survivor option, portability, Social Security, annuity, other reliable income | Dependable income can increase capacity for portfolio risk but does not provide emergency liquidity. | “Do you expect a pension or other dependable income, and what are its vesting, inflation, and survivor terms?” |
| PS-020 | `dependents`: array | children, partner, parents, disabled dependents; support amount and duration | Dependents increase reserve, insurance, estate, and liquidity needs. | “Who depends on your income, assets, or unpaid care?” |
| PS-021 | `insurance`: object | health, disability, term/permanent life, property, liability, long-term care; deductibles | Uninsured risks can overwhelm an otherwise sound portfolio. | “What health, disability, life, property, and liability coverage do you have?” |
| PS-022 | `goals`: array | name, target amount, earliest date, priority, flexibility, funded percentage | Every goal can require a different account and allocation. | “What is the money for, how much is needed, when might it first be used, and can the date or amount change?” |
| PS-023 | `retirement_plan`: object | desired age/date, spending estimate, flexibility, health coverage, withdrawal accounts | Retirement introduces longevity, tax, account-access, and sequence-of-returns risk. | “When might you retire, what spending would be essential, and could you work longer or spend less?” |
| PS-024 | `liquidity_needs`: object | known purchases, tax bills, tuition, moving costs, medical needs, capital calls | Money that may be needed soon should not depend on favorable market performance. | “Which amounts must remain available over the next several years?” |
| PS-025 | `risk_tolerance`: enum/object | low, moderate, high, unknown; reactions to loss scenarios | Measures willingness to accept volatility and loss. | “What decline would make you sell or abandon the plan?” |
| PS-026 | `risk_capacity`: enum/object | low, moderate, high, unknown; modeled separately for each goal | Measures the financial ability to withstand loss without harming essentials or required goals. | “If the investment fell substantially, could you still fund the goal without borrowing or selling?” |
| PS-027 | `knowledge_level`: enum | beginner, intermediate, experienced, professional; product-specific experience | Implementation should be understandable; confidence is not evidence of competence. | “Which investments and account rules can you explain comfortably?” |
| PS-028 | `behavior_history`: object | panic selling, frequent trading, return chasing, leverage, gambling concerns | A theoretically efficient allocation is unsuitable if the user is likely to abandon it. | “Have you sold during a decline, traded frequently, or borrowed to invest?” |
| PS-029 | `values_preferences`: object | ESG, faith screens, exclusions, impact, shareholder engagement | Screens can alter costs, diversification, taxes, and tracking error. | “Do you want any values-based exclusions or impact preferences?” |
| PS-030 | `special_constraints`: set | minor, visa holder, divorce, inheritance, caregiving, disability, benefits eligibility, bankruptcy, legal dispute | Legal, tax, ownership, and benefits consequences can make general guidance inadequate. | “Are there legal, immigration, benefits, family, or health circumstances that constrain the decision?” |
| PS-031 | `contribution_capacity`: currency/time | sustainable recurring amount; possible windfalls; employer payroll constraints | A viable plan depends more on sustainable savings than optimistic returns. | “How much can you invest regularly without using debt or missing essential expenses?” |
| PS-032 | `data_freshness`: date | date profile was confirmed; date of last material life change | Stale facts can make a previously reasonable explanation unsafe. | “When were these balances, benefits, and goals last updated?” |

Profile dimensions are consistent with the customer-profile factors identified in [FINRA Rule 2111](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2111) and the broader circumstances considered by [CFP Board’s standards](https://www.cfp.net/ethics/code-of-ethics-and-standards-of-conduct).

---

<a id="decision-rules"></a>
# DECISION-RULES — If/then guidance

These rules establish educational defaults, not automatic trade instructions. Apply them to each goal and the household’s full balance sheet.

## Foundations and debt

- **R-001:** If investing would cause missed housing, food, utilities, insurance, taxes, or minimum debt payments, pause optional investing and protect those obligations first.  
  *Rationale:* Market exposure cannot repair negative essential cash flow and may compound distress. Source: [CFPB—Your Money, Your Goals](https://www.consumerfinance.gov/consumer-tools/educator-tools/your-money-your-goals/).

- **R-002:** If an affordable employer match is available, generally contribute enough to capture the full match after confirming vesting, payroll, and true-up rules.  
  *Rationale:* The match is compensation, but an unvested or unaffordable contribution is not automatically beneficial. Source: [Investor.gov—Lump-sum payouts and employer plans](https://www.investor.gov/additional-resources/general-resources/publications-research/info-sheets/lump-sum-payouts-questions-1).

- **R-003:** If there is no liquid emergency reserve, build a starter reserve before taxable investing and work toward roughly **three to six months** of essential expenses.  
  *Rationale:* A reserve helps prevent an unexpected expense from becoming debt or a forced sale. Source: [FINRA—Prepare to survive financial hardship](https://www.finra.org/investors/insights/prepare-survive-financial-hardship).

- **R-004:** If income is variable, there is one earner, dependents rely on the income, or a job transition is likely, favor the upper end of the reserve range or more.  
  *Rationale:* Greater cash-flow uncertainty lowers risk capacity. Source: [FINRA—Prepare to survive financial hardship](https://www.finra.org/investors/insights/prepare-survive-financial-hardship).

- **R-005:** If the user has credit-card, payday, or similarly expensive debt, preserve a starter reserve and affordable match, then prioritize the highest APR before investing beyond the match.  
  *Rationale:* Avoided high interest is comparatively certain, while investment returns are uncertain. Source: [Investor.gov—Pay off high-interest debt first](https://www.investor.gov/introduction-investing/investing-basics/save-and-invest/pay-credit-cards-or-other-high-interest-debt).

- **R-006:** If debt is low-rate, fixed, manageable, and protected by adequate reserves, compare repayment with investing instead of applying a blanket “all debt first” rule.  
  *Rationale:* Liquidity, tax treatment, federal protections, and goal dates may be more important than accelerating inexpensive debt. Source: [Investor.gov—Saving and investing roadmap](https://www.investor.gov/introduction-investing/getting-started).

- **R-007:** If student loans may qualify for PSLF or IDR, verify loan type, employer, payment plan, and official payment counts before refinancing or prepaying.  
  *Rationale:* Private refinancing or extra principal can reduce or eliminate valuable federal options. Source: [Federal Student Aid—PSLF](https://studentaid.gov/manage-loans/forgiveness-cancellation/public-service), [Federal Student Aid—IDR](https://studentaid.gov/manage-loans/repayment/plans/income-driven).

- **R-008:** If a credible forgiveness path does not apply and a student loan has a high rate, compare the guaranteed benefit of repayment with the uncertain investment return.  
  *Rationale:* High-rate repayment may improve the balance sheet without market risk. Source: [Federal Student Aid—Repayment plans](https://studentaid.gov/manage-loans/repayment/plans).

- **R-009:** If others depend on the user’s earnings, review health, disability, term-life, beneficiaries, and estate basics before materially increasing investment risk.  
  *Rationale:* The household’s earning capacity is often its largest economic asset. Source: [NAIC—Life insurance](https://content.naic.org/consumer/life-insurance.htm), [CFPB—Your Money, Your Goals](https://files.consumerfinance.gov/f/YMYG_Workers_Toolkit_Emp_4-28-16_machine_readable_a.pdf).

## Goals, horizon, and risk

- **R-010:** If money may be required within **five years or less**, do not rely on risky investments to fund the required amount.  
  *Rationale:* A forced sale after a decline can make the goal unaffordable. Source: [Investor.gov—Gauge your risk tolerance](https://www.investor.gov/introduction-investing/investing-basics/save-and-invest/gauge-your-risk-tolerance).

- **R-011:** If the household has goals with different dates, create separate goal buckets rather than imposing one allocation on every dollar.  
  *Rationale:* Retirement, tuition, and a down payment can have radically different horizons. Source: [Investor.gov—Asset allocation](https://www.investor.gov/introduction-investing/getting-started/asset-allocation).

- **R-012:** If risk tolerance and risk capacity conflict, use the lower one as the risk ceiling.  
  *Rationale:* Willingness cannot make an unaffordable loss affordable, and excessive volatility can cause an investor to abandon the plan. Source: [Investor.gov—Risk tolerance](https://www.investor.gov/introduction-investing/investing-basics/save-and-invest/gauge-your-risk-tolerance).

- **R-013:** If the user is young but needs tuition, rent, moving, or house money soon, treat that money as short-term despite the user’s age.  
  *Rationale:* Horizon belongs to the goal, not the investor’s birth date. Source: [Investor.gov—Asset allocation](https://www.investor.gov/introduction-investing/getting-started/asset-allocation).

- **R-014:** If using an “age minus” stock rule, present it only as a discussion prompt and replace it with goal, pension, liquidity, and risk analysis.  
  *Rationale:* Age-only formulas omit the factors that determine whether losses can be tolerated. Source: [Investor.gov—Asset allocation](https://www.investor.gov/introduction-investing/getting-started/asset-allocation).

- **R-015:** If considering a target-date fund, inspect its current allocation, international exposure, fees, and whether the glide path is designed “to” or “through” retirement.  
  *Rationale:* Funds with the same target year can have different risks and are not guarantees. Source: [Vanguard—Target-date glide path](https://workplace.vanguard.com/investment/strategies/tdf-glide-path.html).

- **R-016:** If withdrawals will begin soon, explicitly address sequence-of-returns risk, spending flexibility, and near-term reserves.  
  *Rationale:* Poor early returns combined with withdrawals can permanently impair the portfolio. Source: [Schwab—Sequence-of-returns risk](https://www.schwab.com/learn/story/timing-matters-understanding-sequence-returns-risk).

- **R-017:** If a pension is reliable, vested, and inflation-protected, it may support more growth risk elsewhere, but do not treat it as liquid cash or ignore survivor and portability terms.  
  *Rationale:* Pension income can be bond-like economically while remaining illiquid and conditional. Source: [Investor.gov—Defined-benefit plans](https://www.investor.gov/introduction-investing/investing-basics/glossary/defined-benefit-plan).

## Accounts and taxes

- **R-018:** If the current marginal tax rate is low relative to the expected future rate, give Roth contributions greater consideration; if it is substantially higher, give traditional contributions greater consideration.  
  *Rationale:* The key comparison is the tax rate paid now versus the rate expected on withdrawal, not average tax rate. Source: [IRS—Roth comparison chart](https://www.irs.gov/retirement-plans/roth-comparison-chart).

- **R-019:** If future tax rates are highly uncertain, consider tax diversification across traditional, Roth, HSA, and taxable assets rather than an all-or-nothing choice.  
  *Rationale:* Multiple tax treatments create withdrawal flexibility. Source: [IRS—Roth comparison chart](https://www.irs.gov/retirement-plans/roth-comparison-chart).

- **R-020:** If a direct Roth IRA contribution may exceed the current MAGI phaseout, verify eligibility before contributing; do not improvise a backdoor Roth without checking the pro-rata rule.  
  *Rationale:* Pre-tax traditional, SEP, or SIMPLE IRA balances can create conversion tax. Source: [IRS Publication 590-A](https://www.irs.gov/publications/p590a).

- **R-021:** If enrolled in an HSA-eligible HDHP and able to cover the deductible, consider an HSA; otherwise compare the health plans on total expected cost and coverage, not tax benefits alone.  
  *Rationale:* The HSA’s tax treatment does not make an unsuitable health plan suitable. Source: [IRS Publication 969](https://www.irs.gov/publications/p969), [HealthCare.gov—HDHPs](https://www.healthcare.gov/high-deductible-health-plan/).

- **R-022:** If a governmental 457(b) and a 401(k) or 403(b) are both available, verify whether their deferral limits are separate and compare fees and withdrawal rules.  
  *Rationale:* A governmental 457(b) can provide additional tax-advantaged capacity and different post-separation access. Source: [IRS—457(b) plans](https://www.irs.gov/retirement-plans/retirement-plans-for-governmental-and-nongovernmental-employers/section-457b-deferred-compensation-plans).

- **R-023:** If the 457(b) is nongovernmental, evaluate employer-creditor risk and distribution restrictions before prioritizing it.  
  *Rationale:* Nongovernmental assets may remain subject to the employer’s creditors. Source: [IRS—457(b) plans](https://www.irs.gov/retirement-plans/retirement-plans-for-governmental-and-nongovernmental-employers/section-457b-deferred-compensation-plans).

- **R-024:** If a goal requires flexible access before retirement, consider a taxable brokerage after foundations rather than forcing every dollar into a restricted retirement account.  
  *Rationale:* Taxable accounts lack retirement-account shelter but provide broad liquidity. Source: [IRS Publication 550](https://www.irs.gov/publications/p550).

- **R-025:** If funding education, protect the investor’s own essential retirement needs before overfunding a 529 and match the 529 allocation to the education date.  
  *Rationale:* Education has alternative funding sources; retirement generally cannot be financed by student aid. Source: [IRS—529 plans](https://www.irs.gov/newsroom/529-plans-questions-and-answers).

- **R-026:** If a teen has genuine taxable compensation, a custodial Roth IRA may be considered; gifts, scholarships, and invented wages do not create contribution room.  
  *Rationale:* IRA contributions require eligible compensation and documentation. Source: [IRS Publication 590-A](https://www.irs.gov/publications/p590a).

## Occupation and human capital

- **R-027:** If salary, career prospects, and investments all depend on one employer or industry, reduce correlated portfolio exposure where practical.  
  *Rationale:* Job loss and asset decline can occur together. Source: [FINRA—Concentration risk](https://www.finra.org/investors/insights/concentration-risk).

- **R-028:** If the user receives RSUs or ESPP shares, treat vested shares as a fresh investment decision and include unvested compensation in concentration analysis.  
  *Rationale:* Employer equity is compensation and single-company risk, not automatically a diversified investment. Source: [IRS Publication 525](https://www.irs.gov/publications/p525), [FINRA—Concentration risk](https://www.finra.org/investors/insights/concentration-risk).

- **R-029:** If self-employed or paid irregularly, reserve taxes and business operating cash before investing variable receipts.  
  *Rationale:* Tax money and operating capital are not long-horizon risk capital. Source: [IRS—Self-employed retirement plans](https://www.irs.gov/retirement-plans/retirement-plans-for-self-employed-people).

- **R-030:** If a physician or other high-income professional relies heavily on future earnings, review individual disability coverage before assuming high risk capacity.  
  *Rationale:* A high salary increases the economic value exposed to disability. Source: [NAIC—Disability insurance](https://content.naic.org/article/consumer-insight-if-disability-were-keep-you-earning-living-how-would-you-pay-your-bills).

- **R-031:** If covered by the military Blended Retirement System, verify and capture the available TSP government contribution when affordable.  
  *Rationale:* TSP matching is part of military compensation, subject to service-specific eligibility and vesting. Source: [TSP—Contributions](https://www.tsp.gov/what-is-contribution/).

- **R-032:** If employment is physically demanding, give additional weight to disability coverage, cash reserves, and possible earlier career transition.  
  *Rationale:* Human capital may be less durable even when current wages are stable. Source: [CFPB—Workers toolkit](https://files.consumerfinance.gov/f/YMYG_Workers_Toolkit_Emp_4-28-16_machine_readable_a.pdf).

## Portfolio construction and behavior

- **R-033:** If the user needs a default core, begin with broad, low-cost domestic stock, international stock, and high-quality bond funds appropriate to the goal.  
  *Rationale:* Broad funds reduce company-specific risk and simplify implementation. Source: [Investor.gov—Diversification](https://www.investor.gov/introduction-investing/getting-started/asset-allocation-diversification-and-rebalancing).

- **R-034:** If two funds are being combined, inspect holdings overlap, sectors, countries, and factor exposure before calling the combination diversified.  
  *Rationale:* Different fund names can conceal substantially identical holdings. Source: [Investor.gov—Diversification](https://www.investor.gov/introduction-investing/getting-started/asset-allocation-diversification-and-rebalancing).

- **R-035:** If selecting a bond fund, match credit quality and duration to the bond allocation’s job; do not describe a bond fund as cash or guaranteed principal.  
  *Rationale:* Bond funds have interest-rate, credit, inflation, and reinvestment risk. Source: [Investor.gov—Bond funds](https://www.investor.gov/introduction-investing/investing-basics/investment-products/bonds-or-fixed-income-products).

- **R-036:** If comparing funds, evaluate the prospectus expense ratio, bid-ask spread, tracking difference, account fees, and tax effects—not expense ratio alone.  
  *Rationale:* Total implementation cost can exceed the stated operating expense. Source: [Investor.gov—Mutual funds and ETFs](https://www.investor.gov/introduction-investing/investing-basics/investment-products/mutual-funds-and-exchange-traded-funds-etfs/mutual-funds), [FINRA Fund Analyzer](https://www.finra.org/investors/tools-and-calculators/finra-fund-analyzer).

- **R-037:** If allocations drift, first use new contributions, distributions, or withdrawals to rebalance and consider tax consequences before selling.  
  *Rationale:* Rebalancing restores intended risk; it is not a response to market headlines. Source: [Investor.gov—Rebalancing](https://www.investor.gov/introduction-investing/getting-started/asset-allocation-diversification-and-rebalancing).

- **R-038:** If a lump sum is genuinely long-term capital and the allocation is tolerable, prompt investment generally provides earlier market exposure; use a short predetermined DCA schedule if it prevents panic or abandonment.  
  *Rationale:* DCA can reduce regret but creates cash drag and does not make a risky allocation safe. Source: [Vanguard—Cost averaging research](https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf).

- **R-039:** If individual stocks are allowed, use broad funds as the core and treat a maximum of **5%** in one self-selected company and **10%** across all self-selected companies as conservative application guardrails, not legal or universal limits.  
  *Rationale:* Single-company risk is uncompensated and can dominate outcomes; stricter treatment may be needed for employer stock. Source and policy context: [FINRA—Concentration risk](https://www.finra.org/investors/insights/concentration-risk).

- **R-040:** If the user wants crypto, options, leverage, or another speculative asset, first fund essentials and the diversified core; use only money whose total loss would not impair a required goal.  
  *Rationale:* Speculation can involve permanent loss, leverage, fraud, custody, tax, and liquidity risks. Source: [FINRA—Crypto assets](https://www.finra.org/investors/investing/investment-products/crypto-assets), [Investor.gov—Margin](https://www.investor.gov/introduction-investing/investing-basics/glossary/margin).

- **R-041:** If the user wants to sell after a decline, first determine whether the goal, liquidity need, or capacity changed; do not reflexively tell the user either to sell or “just hold.”  
  *Rationale:* The original allocation may have been unsuitable, but panic selling can also lock in losses. Source: [Investor.gov—Build wealth over time](https://www.investor.gov/build-wealth-over-time-through-saving-and-investing).

## Special situations and AI controls

- **R-042:** If a home purchase is near or inflexible, keep the required down payment, closing costs, and post-closing reserve in liquid, low-volatility vehicles.  
  *Rationale:* A market decline just before closing can derail the purchase. Source: [CFPB—Buying a house](https://www.consumerfinance.gov/owning-a-home/).

- **R-043:** If the user receives a windfall or inheritance, pause irreversible decisions, secure records, identify taxes and account types, and create a written plan before investing.  
  *Rationale:* Inherited securities, retirement accounts, trusts, and cash have different tax and distribution rules. Source: [FINRA—Sudden wealth](https://www.finra.org/investors/insights/sudden-wealth), [IRS Publication 559](https://www.irs.gov/publications/p559).

- **R-044:** If income is lost or sharply reduced, preserve cash, benefits, health coverage, and minimum payments before continuing optional contributions.  
  *Rationale:* Job loss changes liquidity needs and risk capacity immediately. Source: [Department of Labor—COBRA](https://www.dol.gov/general/topic/health-plans/cobra), [HealthCare.gov—Loss of coverage](https://www.healthcare.gov/have-job-based-coverage/if-you-lose-job-based-coverage/).

- **R-045:** If divorce, incapacity, a trust, special-needs benefits, contested ownership, or an inheritance is involved, pause irreversible transfers and refer to the appropriate attorney or tax professional.  
  *Rationale:* Investment allocation cannot resolve legal title, beneficiary, QDRO, or benefits eligibility. Source: [Department of Labor—QDRO FAQs](https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/resource-center/faqs/qdro), [CFPB—Managing someone else’s money](https://www.consumerfinance.gov/consumer-tools/managing-someone-elses-money/).

- **R-046:** If the user is an international student, visa holder, nonresident, or has foreign accounts or funds, determine tax residency and obtain cross-border tax review before recommending accounts or foreign products.  
  *Rationale:* Immigration status, tax residency, treaty treatment, PFIC rules, and reporting obligations are different questions. Source: [IRS—Taxation of nonresident aliens](https://www.irs.gov/individuals/international-taxpayers/taxation-of-nonresident-aliens), [IRS—PFIC/Form 8621](https://www.irs.gov/forms-pubs/about-form-8621).

- **R-047:** If values-based investing is requested, inspect the methodology, holdings, benchmark, voting policy, turnover, and expense ratio rather than relying on the fund name or ESG score.  
  *Rationale:* Labels and rating systems use different definitions and can conceal concentration. Source: [Investor.gov—Sustainable investing](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/sustainable).

- **R-048:** If a material profile field is missing—especially horizon, liquidity, debt distress, tax status, risk capacity, or concentration—do not provide a specific trade, security, leverage strategy, or precise allocation.  
  *Rationale:* Unsupported personalization can be misleading and may function as a recommendation. Source: [FINRA Rule 2111](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2111).

- **R-049:** If the answer requires a current ticker, price, return, yield, ratio, holdings list, or expense ratio, call the approved lookup tool and display the source and data time.  
  *Rationale:* Dynamic market facts cannot safely be supplied from model memory. Source: [SEC—Market data](https://www.investor.gov/introduction-investing/investing-basics/how-stock-markets-work/market-data).

- **R-050:** If an identifier is ambiguous, data are missing or stale, or sources disagree, state the limitation and do not guess.  
  *Rationale:* A plausible but incorrect ticker or number can cause a harmful transaction. Source: [SEC—Robo-adviser guidance](https://www.sec.gov/files/ib_robo_advisers.pdf).

- **R-051:** If the product gives compensated, individualized securities recommendations or automated portfolio management, do not rely on an “education only” label; obtain securities counsel and operate under the applicable adviser, broker-dealer, and state rules.  
  *Rationale:* Legal classification depends on conduct, compensation, and the complete user experience. Source: [SEC—Robo-adviser guidance](https://www.sec.gov/files/ib_robo_advisers.pdf), [SEC—Regulation Best Interest](https://www.sec.gov/regulation-best-interest).

- **R-052:** If the user cannot pay essentials, is facing eviction, fraud, coercion, bankruptcy, gambling losses, or severe distress, pause investment suggestions and prioritize stabilization and qualified help.  
  *Rationale:* High-risk investing is not a remedy for financial distress. Source: [CFPB—Credit counseling](https://www.consumerfinance.gov/ask-cfpb/what-is-credit-counseling-en-1451/), [HUD—Housing counseling](https://www.hud.gov/counseling).

---

<a id="allocation-convention"></a>
# ALLOCATION-CONVENTION — How to read the playbooks

The ranges below are **illustrative educational ranges for a long-term retirement bucket**, not personalized recommendations, expected-return forecasts, or safe allocations. Cash for emergencies and required near-term goals is separate. Narrow or lower the stock range when risk capacity or tolerance is lower.

The examples are application-created ranges anchored to the diversified allocations illustrated by [Vanguard’s asset-allocation models](https://investor.vanguard.com/investor-resources-education/education/model-portfolio-allocation), its [target-date glide path](https://workplace.vanguard.com/investment/strategies/tdf-glide-path.html), and the SEC’s goal-and-horizon framework in [Investor.gov—Asset allocation](https://www.investor.gov/introduction-investing/getting-started/asset-allocation). They are not claims that a particular mix is optimal.

---

<a id="profile-playbooks"></a>
# PROFILE-PLAYBOOKS — Common archetypes

<a id="pb-001"></a>
## PB-001 — College student with limited savings

**Priorities, in order**

1. Keep tuition, rent, books, transportation, taxes, and emergency money liquid.
2. Avoid investing borrowed money or money needed during school.
3. Pay expensive revolving debt.
4. Capture an affordable workplace match.
5. If there is genuine taxable compensation, consider a Roth IRA for money that can remain invested for decades.
6. Use one broad diversified fund or a low-cost target-date fund rather than stock picking.

**Illustrative allocation**

- Near-term education and living money: cash or cash-like instruments, not stocks.
- Long-term retirement bucket: **80%–100% diversified stocks and 0%–20% high-quality bonds**, subject to the student’s actual capacity and tolerance. The range is centered on Vanguard’s published age-20 target-date example of approximately **90% stocks**. Source: [Vanguard—Target-date glide path](https://workplace.vanguard.com/investment/strategies/tdf-glide-path.html).

**Account order**

Cash reserve → affordable employer match → Roth IRA if compensation and eligibility permit → additional workplace plan → taxable account for genuinely long-term flexible money.

**Pitfalls**

Investing tuition, using margin, treating scholarships or gifts as IRA compensation, frequent trading, and assuming youth creates unlimited risk capacity.

---

<a id="pb-002"></a>
## PB-002 — New graduate or early-career worker

**Priorities, in order**

1. Fund relocation and a liquid reserve.
2. Capture the employer match.
3. Eliminate high-interest consumer debt.
4. Establish health and disability coverage.
5. Create separate buckets for retirement, a vehicle, home purchase, and other goals.
6. Automate diversified contributions and increase them with income.

**Illustrative allocation**

- Long-term retirement bucket: **70%–90% stocks and 10%–30% high-quality bonds**.
- A home or other inflexible goal within **five years or less** should not depend on stocks. Source: [Vanguard—Allocation models](https://investor.vanguard.com/investor-resources-education/education/model-portfolio-allocation), [Investor.gov—Risk tolerance](https://www.investor.gov/introduction-investing/investing-basics/save-and-invest/gauge-your-risk-tolerance).

**Account order**

Workplace plan to match → HSA if the health plan fits → Roth or deductible traditional IRA → additional workplace contributions → taxable brokerage for flexible goals.

**Pitfalls**

Lifestyle inflation, aggressive investing before building cash, carrying employer or sector concentration, and using retirement accounts for an imminent down payment.

---

<a id="pb-003"></a>
## PB-003 — Resident doctor with large student loans

**Priorities, in order**

1. Use resident income—not expected attending income—to set spending.
2. Verify PSLF, IDR, employer, loan type, and payment counts before refinancing or prepaying.
3. Keep relocation, licensing, exam, and emergency cash.
4. Capture any retirement-plan match.
5. Review own-occupation disability coverage and employer limitations.
6. Consider Roth contributions during a temporarily lower tax-bracket period.
7. Raise savings automatically when attending income begins.

**Illustrative allocation**

- Long-term retirement bucket: **70%–90% stocks and 10%–30% bonds**, only after separating cash needed for training and transitions. Source: [Vanguard—Allocation models](https://investor.vanguard.com/investor-resources-education/education/model-portfolio-allocation).

**Account order**

Required loan payment and verified forgiveness strategy → workplace match → HSA if appropriate → Roth IRA if eligible → additional 401(k)/403(b) contributions → taxable account.

**Pitfalls**

Refinancing federal loans without PSLF review, assuming future salary is guaranteed, underinsuring disability, or making speculative bets to “catch up.”

---

<a id="pb-004"></a>
## PB-004 — Attending physician or other high-income professional

**Priorities, in order**

1. Maintain reserves and adequate disability, liability, and life coverage.
2. Finalize the student-loan strategy.
3. Automate retirement saving before lifestyle spending expands.
4. Use tax-advantaged accounts and model traditional-versus-Roth contributions.
5. Diversify practice ownership, real estate, and other concentrated assets.
6. Build taxable assets for flexibility and goals before retirement age.

**Illustrative allocation**

- Long-term bucket: **70%–90% stocks and 10%–30% bonds** for high capacity and tolerance; use a lower stock percentage when income is concentrated, debt is large, or near-term purchases are material. Source: [Vanguard—Allocation models](https://investor.vanguard.com/investor-resources-education/education/model-portfolio-allocation).

**Account order**

Workplace match → HSA if suitable → workplace plan, often with traditional contributions considered in a high current bracket → IRA strategy after eligibility/pro-rata review → governmental 457(b) if available and suitable → taxable brokerage.

**Pitfalls**

Confusing high income with high capacity, unsupported backdoor Roth transactions, permanent-life products sold primarily as investments, and excessive practice or real-estate concentration.

---

<a id="pb-005"></a>
## PB-005 — Teacher or public worker with a pension

**Priorities, in order**

1. Understand pension vesting, formula, retirement age, COLA, survivor benefits, portability, and Social Security interaction.
2. Keep liquid assets outside the pension.
3. Capture any match.
4. Compare 403(b) and governmental 457(b) menus and fees.
5. Avoid high-cost annuity contracts solely because they are offered at work.
6. Coordinate investment risk with pension reliability rather than counting the pension at face value.

**Illustrative allocation**

- Long-term financial portfolio: **60%–90% stocks and 10%–40% bonds**. A strong vested inflation-adjusted pension may support the upper part of the range; an unvested or weakly protected pension should not. Source: [Vanguard—Allocation models](https://investor.vanguard.com/investor-resources-education/education/model-portfolio-allocation), [Investor.gov—Defined-benefit plan](https://www.investor.gov/introduction-investing/investing-basics/glossary/defined-benefit-plan).

**Account order**

403(b) or 457(b) match → HSA if eligible and suitable → low-cost IRA → additional low-cost 403(b) and/or governmental 457(b) → taxable brokerage.

**Pitfalls**

Assuming the pension is liquid or guaranteed in every circumstance, ignoring vesting, buying a costly annuity without comparison, and missing separate 403(b)/457(b) opportunities.

---

<a id="pb-006"></a>
## PB-006 — Nurse who is a single parent

**Priorities, in order**

1. Maintain a larger reserve for childcare, deductibles, leave, and income disruption.
2. Review health, disability, and term-life coverage and guardianship/beneficiaries.
3. Base recurring contributions on ordinary wages, not overtime.
4. Capture the match and eliminate expensive debt.
5. Invest bonuses or overtime only after reserve and tax needs.
6. Fund education goals only after protecting the parent’s retirement foundation.

**Illustrative allocation**

- Long-term retirement bucket: **60%–80% stocks and 20%–40% bonds**, with the lower end appropriate when reserves, coverage, or job flexibility are limited. Source: [Vanguard—Allocation models](https://investor.vanguard.com/investor-resources-education/education/model-portfolio-allocation).

**Account order**

Emergency and insurance foundation → workplace match → HSA if the health plan fits → IRA → additional workplace plan → 529 after retirement is on track → taxable account.

**Pitfalls**

Basing fixed spending on overtime, inadequate disability or life coverage, investing childcare money, and overfunding college while underfunding retirement.

---

<a id="pb-007"></a>
## PB-007 — Technology worker with RSUs or ESPP shares

**Priorities, in order**

1. Map salary, unvested awards, vested shares, options, ESPP, and sector funds as one exposure.
2. Reserve for tax obligations and verify withholding.
3. Establish a written diversification policy for shares as they vest.
4. Capture the retirement match and build a broad fund core.
5. Model option exercises and private-company equity with a tax professional when material.
6. Do not count an expected IPO or acquisition as liquid wealth.

**Illustrative allocation**

- Diversified long-term portfolio, after counting employer stock: **60%–85% stocks and 15%–40% bonds**.
- As an application guardrail, keep one self-selected company at no more than **5%** and all self-selected companies at no more than **10%** of investable financial assets, with stricter treatment for employer stock. Source: [Vanguard—Allocation models](https://investor.vanguard.com/investor-resources-education/education/model-portfolio-allocation), [FINRA—Concentration risk](https://www.finra.org/investors/insights/concentration-risk).

**Account order**

401(k) match → HSA if suitable → IRA after eligibility review → additional 401(k) → ESPP only with a documented sale/concentration policy → taxable diversified investments.

**Pitfalls**

Treating vested shares as free money, relying on inadequate tax withholding, borrowing to exercise illiquid options, and combining career risk with a technology-heavy portfolio.

---

<a id="pb-008"></a>
## PB-008 — Gig worker or self-employed person

**Priorities, in order**

1. Separate business and personal finances.
2. Reserve federal, state, and self-employment taxes.
3. Maintain operating cash plus a larger personal reserve.
4. Obtain health, disability, liability, and dependent protection.
5. Use a conservative income baseline for recurring contributions.
6. Select among Solo 401(k), SEP-IRA, SIMPLE IRA, or another plan based on employees, Roth needs, contribution flexibility, and administration.

**Illustrative allocation**

- Long-term bucket: **50%–80% stocks and 20%–50% bonds**, depending on income volatility and reserve strength. Business cash and tax reserves remain outside the portfolio. Source: [Vanguard—Allocation models](https://investor.vanguard.com/investor-resources-education/education/model-portfolio-allocation).

**Account order**

Tax and operating reserves → insurance → HSA if eligible and suitable → Solo 401(k), SEP-IRA, SIMPLE IRA, or IRA as applicable → taxable brokerage.

**Pitfalls**

Investing tax money, failing to account for employees in plan selection, missing plan filings, using a strong month as the recurring baseline, and overlooking the backdoor-Roth effect of SEP/SIMPLE IRA balances.

---

<a id="pb-009"></a>
## PB-009 — Military member under BRS

**Priorities, in order**

1. Confirm the retirement system, TSP matching eligibility, and vesting.
2. Capture the full available government contribution when affordable.
3. Maintain deployment, relocation, and transition reserves.
4. Pay expensive consumer debt.
5. Choose Traditional versus Roth TSP with taxable pay, combat-zone pay, state residence, and expected future rates in mind.
6. Review beneficiaries before deployment and major family changes.

**Illustrative allocation**

- Long-term TSP/retirement bucket: **70%–90% stocks and 10%–30% bonds**, or an appropriate Lifecycle Fund, subject to service horizon and tolerance. Source: [Vanguard—Allocation models](https://investor.vanguard.com/investor-resources-education/education/model-portfolio-allocation), [TSP—Lifecycle funds](https://www.tsp.gov/funds-lifecycle/).

**Account order**

TSP to full BRS contribution → IRA if eligible → additional TSP → taxable account for transition or pre-retirement flexibility.

**Pitfalls**

Assuming a future pension is secured before eligibility, ignoring high-interest debt, overconcentrating in one TSP fund, and rolling out of the TSP without comparing fees and protections.

---

<a id="pb-010"></a>
## PB-010 — Pre-retiree behind on savings

**Priorities, in order**

1. Estimate essential and discretionary retirement spending.
2. Inventory Social Security, pension, health coverage, debts, and all accounts.
3. Increase sustainable savings, use applicable catch-up provisions, reduce expenses, and consider working longer.
4. Do not attempt to close the gap with leverage or concentrated stocks.
5. Create a withdrawal and reserve plan for the first retirement years.
6. Model taxes, Social Security timing, and adverse market scenarios with a qualified planner.

**Illustrative allocation**

- Long-term portfolio: **40%–65% stocks and 35%–60% bonds**, with required near-term withdrawals held separately in cash and short-duration high-quality assets. Source: [Vanguard—Target-date glide path](https://workplace.vanguard.com/investment/strategies/tdf-glide-path.html), [Schwab—Sequence risk](https://www.schwab.com/learn/story/timing-matters-understanding-sequence-returns-risk).

**Account order**

Workplace match → applicable catch-up contributions → HSA if eligible → IRA if eligible → additional workplace plan → taxable reserves. Coordinate rather than automatically liquidating old accounts.

**Pitfalls**

Taking more risk because savings are low, ignoring health-care costs, eliminating all stocks and creating inflation risk, or claiming a retirement date is guaranteed.

---

<a id="pb-011"></a>
## PB-011 — Retiree drawing from a portfolio

**Priorities, in order**

1. Separate essential from discretionary spending.
2. Map pension, Social Security, RMDs, and other dependable income.
3. Maintain liquid reserves so essential spending does not require selling stocks after a decline.
4. Retain diversified growth exposure for inflation and longevity.
5. Coordinate taxable, traditional, Roth, and HSA withdrawals.
6. Review beneficiaries, powers of attorney, fraud controls, and long-term-care planning.

**Illustrative allocation**

- Long-term portfolio: **30%–60% stocks and 40%–70% bonds**, plus a goal-specific cash reserve.
- One planning example is approximately **one year** of spending needs after dependable income in cash and another **two to four years** in high-quality short-term bonds; this is not a universal requirement. Source: [Vanguard—Target-date glide path](https://workplace.vanguard.com/investment/strategies/tdf-glide-path.html), [Schwab—Sequence risk](https://www.schwab.com/learn/story/timing-matters-understanding-sequence-returns-risk).

**Account/withdrawal order**

There is no universal withdrawal sequence. Coordinate current cash, taxable gains, traditional distributions, RMDs, Roth assets, HSA reimbursements, bracket management, Medicare effects, and estate goals with a tax professional.

**Pitfalls**

Selling stocks mechanically after a decline, moving everything to cash, treating dividend yield as a substitute for total return, ignoring taxes, and falling for fraud or high-pressure annuity sales.

---

<a id="mcp-lookup-guide"></a>
# MCP-LOOKUP-GUIDE — Live stock and fund data

<a id="mcp-when"></a>
## MCP-WHEN — When to call the lookup tool

Call the approved MCP tool whenever the answer depends on:

- A ticker, issuer, exchange, share class, fund, ETF, mutual fund, or security identifier.
- Current or historical price, NAV, total return, market capitalization, assets under management, yield, valuation, beta, expense ratio, spread, premium/discount, or holdings.
- Comparing two funds’ holdings, concentration, sector/country weights, costs, or overlap.
- Verifying whether an instrument exists, is listed, has been delisted, or is the security the user intended.
- Confirming a current fund benchmark, strategy, leverage, distribution policy, or share-class fee.

Do not call the market-data tool merely to explain stable concepts such as diversification. Tax and regulatory facts should come from current IRS, SEC, FINRA, Department of Labor, Federal Student Aid, or other primary documents rather than a securities quote tool.

<a id="mcp-identity"></a>
## MCP-IDENTITY — Resolve the instrument first

Fetch and display:

- Legal issuer or fund name.
- Ticker and canonical identifier.
- Exchange, security type, share class, currency, and listing status.
- For funds: sponsor, benchmark, inception date, active/index status, and whether it is leveraged, inverse, thematic, or target-date.
- Provider, retrieval timestamp, field-level as-of times, timezone, and whether data are real-time, delayed, end-of-day, or stale.

If the ticker is ambiguous, delisted, non-US, or inconsistent with the user’s description, ask the user to clarify. Never guess.

<a id="mcp-fields"></a>
## MCP-FIELDS — Fields to fetch

### For a stock

- Price and prior close, with timestamp and market status.
- Market capitalization and shares outstanding, if available.
- Trailing and forward P/E, clearly distinguished.
- Earnings period and whether earnings are positive.
- Dividend yield, dividend history, and methodology.
- Beta, benchmark, and lookback period.
- Revenue, earnings, cash flow, and debt data from the latest applicable filing.
- Sector, industry, country, exchange, and currency.
- Corporate actions, split adjustment status, and filing dates.
- The stock’s weight in the user’s funds, when checking overlap or concentration.

### For a mutual fund or ETF

- NAV and market price where applicable.
- Gross and net expense ratios and waiver expiration.
- Benchmark, strategy, asset class, and index methodology.
- Assets under management and share class.
- Full or latest available holdings date.
- Top holdings and weights; sector, country, currency, and asset-class exposure.
- Number of holdings, while noting that count alone does not establish diversification.
- Portfolio P/E and the provider’s treatment of negative earnings.
- Distribution yield, SEC yield where applicable, and methodology.
- Beta, benchmark, and lookback period.
- Total returns net of fund operating expenses, with periods and as-of date.
- For bond funds: duration, maturity, credit quality, SEC yield, and tax status.
- For ETFs: bid-ask spread, premium/discount to NAV, and trading liquidity.
- For target-date funds: current allocation, underlying funds, fees, target year, and “to” versus “through” glide path.
- Pairwise and whole-portfolio holdings overlap when comparing funds.

<a id="mcp-interpretation"></a>
## MCP-INTERPRETATION — Interpretation rules

| Field | Correct interpretation | Misinterpretations to prevent |
|---|---|---|
| Expense ratio | Annual fund operating expenses as a percentage of average assets; compare gross/net ratios, waivers, tracking, spreads, and account costs. | It is not applicable to an operating company. A stock showing zero expense ratio does not mean investing is cost-free. |
| P/E | A relative valuation descriptor based on price and earnings; identify trailing versus forward. | A low P/E does not prove “cheap,” and a high P/E does not prove a decline. Negative earnings can make it meaningless. |
| Dividend yield | Income relative to current price under a stated trailing or forward methodology. | It is not total return or a guarantee. A high yield can reflect a collapsing price or an unsustainable payout. |
| Beta | Historical sensitivity to a stated benchmark over a stated period. | It is not a forecast, maximum-loss estimate, or complete measure of company, liquidity, or gap risk. |
| Holdings | A dated look-through of what a fund owns. | A large holdings count does not prevent top-heavy, sector, country, duration, or currency concentration. |
| Overlap | Shared exposure under the provider’s stated formula. | Different names do not guarantee diversification; identical names do not imply identical weights or risks. |
| Price/NAV | A dated observation, not an execution promise. | Do not call delayed data “live”; spreads, order type, fees, and market movement affect execution. |
| Historical return | Past total return over a defined period, ideally including distributions. | It is not an expected return or evidence the asset will continue outperforming. |
| SEC yield | A standardized historical yield calculation for applicable funds. | It is not a guaranteed future distribution or total return. |
| Duration | Approximate price sensitivity to interest-rate changes. | It is not maturity, a guarantee, or the only source of bond-fund risk. |

Sources: [Investor.gov—Mutual funds](https://www.investor.gov/introduction-investing/investing-basics/investment-products/mutual-funds-and-exchange-traded-funds-etfs/mutual-funds), [FINRA Fund Analyzer](https://www.finra.org/investors/tools-and-calculators/finra-fund-analyzer), [FINRA—Concentration risk](https://www.finra.org/investors/insights/concentration-risk).

<a id="mcp-red-flags"></a>
## MCP-RED-FLAGS — What to surface

- Unknown, ambiguous, delisted, or mismatched identifier.
- Missing, stale, incompatible, or provider-disputed timestamps.
- Gross/net expense-ratio mismatch or expiring fee waiver.
- High bid-ask spread or persistent ETF premium/discount.
- Narrow sector, theme, country, employer, or top-holding concentration.
- Substantial overlap with existing funds.
- Leveraged, inverse, derivative-heavy, or path-dependent strategy.
- Negative earnings paired with a displayed or meaningless P/E.
- High dividend yield caused by price decline or an unstable distribution.
- Bond fund with duration or credit risk inconsistent with the goal.
- Fund name or ESG label inconsistent with actual holdings.
- Different fields drawn from