# Getting Started - 10 Minutes to PrismStudio

# 데이터 추출 📤

## 1. 종가 데이터 - 세 줄의 코드로 데이터 추출하기

PrismStudio에서는 아래처럼 세 줄의 코드면 종가 데이터를 추출할 수 있습니다.
Self-contained 코드이기 때문에, 로그인 정보를 업데이트한 후 그대로 사용자의 Python 환경에 복사하여 실행할 수 있습니다.

```{note}
:class: prism-one-line-note
<div>
    <img src="../_static/one-line-info.svg" width="15px" height="15px" />
</div>

**예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)**
```

```python
>>> import prism

>>> prism.login(username="my_username", password="my_password")
>>> close = prism.market.close()
>>> close_data = close.get_data(universe="S&P 500", startdate="2010-01-01", enddate="2020-01-01")
```

이제 PrismStudio에서 어떻게 종가 데이터를 추출할 수 있는지 자세히 살펴보겠습니다.

### 1.1 패키지 불러오기 및 로그인

패키지 설치를 마친 후에 prism 패키지를 불러오면 PrismStudio Python Extension 사용 준비가 완료됩니다.

[login](<#login>) 함수에 미리 제공 받은 로그인 정보를 입력하면 로그인할 수 있습니다.

```python
>>> import prism

>>> prism.login(username="my_username", password="my_password")
```

### 1.2 데이터 선택

주가, 시가총액, 재무, 추정치 등 보유한 데이터 중 관심 있는 데이터를 선택하세요.

예시에서는 종가 데이터를 선택합니다.

```python
>>> close = prism.market.close()
```

(DataExtraction)=

### 1.3 데이터 추출

선택한 데이터에 유니버스 및 데이터 기간을 입력하면 데이터를 추출할 수 있습니다.

S&P 500 유니버스 구성 종목에 대해서 2010년 1월 1일 ~ 2020년 1월 1일 기간에 해당하는 종가 데이터를 추출하며, 추출된 데이터는 close_data 변수에 저장됩니다.

```python
>>> close_data = close.get_data(universe="S&P 500", startdate="2010-01-01", enddate="2020-01-01")
```

## 2. ROA - 데이터 간 연산 수행하기

PrismStudio에서는 단순 데이터 추출은 물론, 연산이 적용된 복잡한 데이터의 추출도 지원합니다.

아래 예시는 Net Income과 Total Assets 데이터에 연산을 수행하여 ROA 데이터를 추출하는 코드입니다.

```{note}
:class: prism-one-line-note
<div>
    <img src="../_static/one-line-info.svg" width="15px" height="15px" />
</div>

**예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)**
```

```python
>>> import prism

>>> prism.login(username="my_username", password="my_password")
>>> ni = prism.financial.income_statement(100639, periodtype="LTM") # 100639: Net Income
>>> ta = prism.financial.balance_sheet(100033, periodtype="Q") # 100033: Assets, Total
>>> roa = ta/ni
>>> roa_data = roa.get_data(universe="S&P 500", startdate="2010-01-01", enddate="2020-01-01"**)**
```

이제 PrismStudio에서 어떻게 ROA 데이터를 추출할 수 있는지 자세히 살펴보겠습니다.

### 2.1 데이터 검색

재무, 추정치 데이터 추출에는 데이터의 ID(dataitemid) 정보가 필요하며, PrismStudio의 Data Items 사이트를 통해 이 정보를 쉽고 빠르게 찾을 수 있습니다.

[prism.dataitem_search](<#prism.dataitem_search>) 함수를 실행하면 Data Items 사이트(아래 그림)로 이동하여 원하는 데이터를 검색하고 ID를 파악할 수 있습니다.

검색 결과, Net Income의 dataitemid는 100639, Total Asset의 dataitemid는 100033입니다.

```python
>>> prism.dataitem_search()
```

> **_Data Items 사이트 화면_**

![DataItemSearch Page Screenshot](../_static/dataitemsearch-screenshot-1.png)

### 2.2 데이터 선택

Data Items 사이트에서 찾은 dataitemid를 사용하여 데이터를 선택합니다.

Net Income은 Financial (Category) > Income Statement (Component)의 data item이기 때문에 [prism.financial.income_statement](<#prism.financial.income_statement>) 함수를 사용합니다.

Total Asset은 Financial (Category) > Balance Sheet (Component)의 data item이기 때문에 [prism.financial.balance_sheet](<#prism.financial.balance_sheet>) 함수를 사용합니다.

```python
>>> ni = prism.financial.income_statement(100639, periodtype='LTM') # 100639: Net Income
>>> ta = prism.financial.balance_sheet(100033, periodtype='Q') # 100033: Assets, Total
```

> **_Data Items 사이트 화면_**

![DataItemSearch Page Screenshot](../_static/dataitemsearch-screenshot-2.png)

(DataOperationExtraction)=

### 2.3 데이터 연산 및 추출

PrismStudio에서는 연산이 적용된 복잡한 데이터의 추출도 지원합니다.

ROA를 계산하기 위해 Net Income을 Total Assets로 나누는 연산을 수행하고, [1.3 데이터 추출](DataExtraction)과 동일한 방법으로 데이터를 추출합니다.

```python
>>> roa = ta/ni
>>> roa_data = roa.get_data(universe="S&P 500", startdate="2010-01-01", enddate="2020-01-01")
```

PrismStudio에서는 Python의 기본 연산은 물론 횡단면 연산, 시계열 연산 등의 고급 연산도 지원합니다. ([PrismStudio에서 지원하는 함수 목록 보기](../apiref/index.rst))

### 2.4 복수의 데이터 추출

한 번에 여러 종류의 데이터를 추출할 수 있습니다.

[prism.get_data](<#prism.get_data>)에 component 파라미터를 추가하고 원하는 데이터를 리스트 형태로 입력하면, 데이터 추출 결과를 튜플 형태로 반환합니다.

```python
>>> ni, ta = prism.get_data(component=[ni, ta], universe="S&P 500", startdate="2010-01-01", enddate="2020-01-01")
```

---

# 스크린 📊

## 1. 유니버스 필터

시큐리티 마스터에서 메타 데이터에 간단한 규칙을 적용하여 신규 유니버스를 만들 수 있습니다.

아래 코드는 한국거래소에서 거래되는 종목을 신규 유니버스로 저장합니다.

```{note}
:class: prism-one-line-note
<div>
    <img src="../_static/one-line-info.svg" width="15px" height="15px" />
</div>

**예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)**
```

```python
>>> import prism

>>> prism.login(username="my_username", password="my_password")

>>> prism.filter_universe(attribute="MIC", value="XKRX", universename="my_krx") # MIC 코드가 XKRX인 종목을 신규 유니버스로 저장합니다.
```

## 2. 스크린 기본

유니버스 편입 규칙을 생성하고 이를 바탕으로 종목을 스크리닝 합니다.

아래 코드는 한국거래소에서 거래되는 종목 중 금융 섹터를 제외하고, 시가총액 상위 200개 종목을 신규 유니버스로 저장합니다.

```{note}
:class: prism-one-line-note
<div>
    <img src="../_static/one-line-info.svg" width="15px" height="15px" />
</div>

**예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)**
```

```python
>>> import prism

>>> prism.login(username="my_username", password="my_password")

>>> non_financial_rule = prism.securitymaster.attribute(attribute="GICS Sector") != "40" # 금융 섹터를 포함하지 않습니다.
>>> mcap = prism.market.market_cap()
>>> marketcap_rule = mcap.cross_sectional_rank() <= 200 # 주어진 날짜에 시가총액 상위 200개를 포함합니다.

# 위의 두 규칙을 적용하여 스크린 태스크 컴포넌트를 생성합니다.
>>> krx_200_screen = prism.screen(
        rule=non_financial_rule & marketcap_rule, # 두 룰을 모두 적용합니다.
        universename="krx", # 기존에 이미 만들어진 krx 유니버스를 스크린 대상으로 합니다.
        startdate="2010-01-01",
        enddate="2015-01-01",
        frequency="D",
        )

# 스크린으로 생성되는 신규 유니버스의 이름을 입력하고 태스크를 실행합니다.
>>> krx_200_screen.run(newuniversename="krx_primary_top200_nonfinancial")
```

### 2.1 규칙 생성

우선 유니버스 편입 규칙을 생성해야 하는데, 이 규칙은 각 종목의 유니버스 편입 여부를 나타내는 불리언(boolean) 형태의 데이터를 말합니다.

예시에서는 금융 섹터 종목을 유니버스에서 제외하기 위해 GICS Sector 값 중 40을 제외하는 규칙을 생성합니다.

또한 시가총액 상위 200개 기업을 유니버스에 포함하기 위해 시가총액 횡단면 순위 값 중 200 이내를 선택하는 규칙을 생성합니다.

```python
>>> non_financial_rule = prism.securitymaster.attribute(attribute="GICS Sector") != "40" # 금융 섹터를 포함하지 않습니다.
>>> mcap = prism.market.market_cap()
>>> marketcap_rule = mcap.cross_sectional_rank() <= 200 # 주어진 날짜에 시가총액 상위 200개를 포함합니다.
```

### 2.2 스크리닝

스크린 함수에 유니버스 및 데이터 기간을 입력하고, 스크린으로 생성되는 신규 유니버스의 이름을 입력하여 스크린을 실행하세요.

[유니버스 리스트](<#prism.list_universe>) 혹은 [유니버스 데이터 가져오기](<#prism.get_universe>)를 통해서 생성된 유니버스를 확인하거나 사용할 수 있습니다.

예시에서는 금융 섹터 제외 규칙 및 시가총액 상위 200개 포함 규칙을 적용하여 스크리닝 합니다.

```python
# 위 두 규칙을 적용하여 스크린 태스크 컴포넌트를 생성합니다.
>>> krx_200_screen = prism.screen(
        rule=non_financial_rule & marketcap_rule, # 두 룰을 모두 적용합니다.
        universename="krx", # 기존에 이미 만들어진 krx 유니버스를 스크린 대상으로 합니다.
        startdate="2010-01-01",
        enddate="2015-01-01",
        frequency="D",
        )

# 스크린으로 생성되는 신규 유니버스의 이름을 입력하고 태스크를 실행합니다.
>>> krx_200_screen.run(newuniversename="krx_primary_top200_nonfinancial")
```

# 팩터 백테스트 📇

## 1. 팩터 백테스트

팩터를 생성하고 이를 이용하여 백테스트 합니다.

아래는 [2.3 데이터 연산 및 추출](DataOperationExtraction)에서 다뤘던 ROA 데이터를 활용하여 팩터 백테스트 하는 코드입니다.

```{note}
:class: prism-one-line-note
<div>
    <img src="../_static/one-line-info.svg" width="15px" height="15px" />
</div>

**예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)**
```

```python
>>> import prism

>>> prism.login(username="my_username", password="my_password")
>>> ni = prism.financial.income_statement(100639, periodtype='LTM') # 100639: Net Incomes
>>> ta = prism.financial.balance_sheet(100033, periodtype='Q') # 100033: Total Assets
>>> roa = ni/ta
>>> roa_fb = prism.factor_backtest(roa, "S&P 500", 'Q', 10, '2010-01-01', '2015-01-01')
>>> roa_fb.run()
```

### 1.1 팩터 생성

PrismStudio에서는 모든 수치 데이터를 팩터로 사용할 수 있습니다.

[2.3 데이터 연산 및 추출](DataOperationExtraction)과 동일하게 ROA 데이터를 선택하면 이를 바로 팩터로 사용할 수 있습니다.

```python
>>> ni = prism.financial.income_statement(100639, periodtype='LTM') # 100639: Net Incomes
>>> ta = prism.financial.balance_sheet(100033, periodtype='Q') # 100033: Total Assets
>>> roa = ni/ta
```

### 1.2 백테스트

팩터 백테스트 함수에 유니버스, 리밸런싱 주기, bin의 개수 및 데이터 기간을 입력하여 백테스트 하세요.

[팩터 백테스트 결과 가져오기](<#prism.get_factor_backtest_result>)를 통해서 백테스트 결과를 분석할 수 있습니다.

```python
>>> roa_fb = prism.factor_backtest(roa, "S&P 500", 'Q', 10, '2010-01-01', '2015-01-01')
>>> roa_fb.run()
```

---

# Job Manager 🗃

Job Manager 사이트에서 스크린 혹은 팩터 백테스트와 같은 태스크의 실행 이력 및 결과를 조회하고 분석할 수 있습니다.

## 1 Job Manager 실행

[prism.job_manager](<#prism.job_manager>) 함수를 실행하면 Job Manager 사이트(아래 그림)로 이동하여 원하는 태스크의 실행 이력 및 결과를 조회할 수 있습니다.

```{note}
:class: prism-one-line-note
<div>
    <img src="../_static/one-line-info.svg" width="15px" height="15px" />
</div>

**예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)**
```

```python
>>> import prism

>>> prism.login(username="my_username", password="my_password")
>>> prism.job_manager()
```

> **_Job Manager 사이트 화면_**

![JobManager Page Screenshot](../_static/jobmanager-screenshot.png)

## 2 리포트 조회

Job Manager 사이트에서는 팩터 백테스트 실행 후 생성되는 리포트를 조회할 수 있습니다.

리포트 조회를 원하는 팩터 백테스트 행에서 “Report” 버튼을 클릭하면 해당 백테스트 결과를 분석할 수 있는 리포트를 확인할 수 있습니다.

> **_팩터 백테스트 리포트 화면_**

![FactorBacktest Screenshot](../_static/factorbacktest-screenshot.png)
