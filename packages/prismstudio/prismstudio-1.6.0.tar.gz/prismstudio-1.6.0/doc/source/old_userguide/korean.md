# User Guide

# 🚀 **시작하기**

PrismStudio 서비스는 Data Enablement 기술을 바탕으로 금융 데이터 업무를 자동화함으로써 금융회사가 더욱 효율적인 데이터 업무 환경을 조성하도록 돕습니다.

사용자는 PrismStudio를 통해 보다 높은 효율성, 정확성, 신뢰성을 가진 데이터 환경을 구축할 수 있고, 이를 바탕으로 더 본질적이고 창의적인 업무에 집중할 수 있습니다.

---

# 🛠 필수 기능

## 검색 작업

쿼리, 유니버스, 포트폴리오 등의 작업 수행을 용이하게 하기 위해 여러 검색 기능을 지원합니다.

시큐리티 마스터, 데이터 아이템, 쿼리, 유니버스, 포트폴리오 등을 검색할 수 있습니다.

### 시큐리티 마스터 검색

시큐리티 마스터 검색에서는 종목 식별자와 메타 데이터의 검색을 제공합니다.

검색하기 위해서는 [prismstudio.get_securitymaster](<#prismstudio.get_securitymaster>) 함수에 검색 기준이 될 식별자 및 메타 데이터의 종류(attribute)를 정한 후 검색하기 원하는 값을 입력하면 됩니다.

예를 들어, 아래 예제 코드처럼 회사명(Company Name)이라는 attribute에 삼성(Samsung)이 포함된 종목을 검색할 수 있습니다.

[prismstudio.securitymaster.list_attribute](<#prismstudio.securitymaster.list_attribute>) 함수를 실행하면 현재 사용할 수 있는 attribute의 종류를 파악할 수 있습니다.

```{dropdown} 사용 가능한 식별자 및 메타 데이터의 종류(attribute)는 아래와 같습니다.
Barra ID, CINS, CIQ Primary, CMA Entity ID, CUSIP, Company ID, Company Name, Composite FIGI, Compustat Primary, Country, FIGI, Factset Company ID, Factset Entity ID, Factset Listing ID, Facset Security ID, Fitch Issuer ID, GICS Group, GICS Industry, GICS Sector, GICS Sub-Industry, GVKEY, GVKEYIID, IBES Ticker, ISIN, LEI, MIC, MarkIt Red Code, Moody’s Issuer Number,  NAICS, RatingXpress Entity ID, SEDOL, SIC, SNL Institution ID, Security ID, Share Class FIGI, Ticker, Trade Currency, Trading Item ID, VALOR, WKN
```

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.securitymaster.list_attribute() # PrismStudio에서 사용 가능한 식별자 종류를 나열합니다.
>>> ps.get_securitymaster(attribute="Company Name", search="Samsung") # 회사 이름(Company Name)에 Samsung이 들어가는 시큐리티 마스터 항목 검색합니다.
      listingid	       valuetype      value   startdate     enddate
   0    2647420  Trading Item ID    2647420  1700-01-01  2199-12-31
   1   20174680  Trading Item ID   20174680  1700-01-01  2199-12-31
   2   30562725  Trading Item ID   30562725  1700-01-01  2199-12-31
   3    2647422  Trading Item ID    2647422  1700-01-01  2199-12-31
   4   30562723  Trading Item ID   30562723  1700-01-01  2199-12-31
 ...        ...              ...        ...         ...	        ...
2050  684446517       	GVKEYIID  33950601W  1700-01-01  2199-12-31
2051  557301422         GVKEYIID  32815501W  1700-01-01  2199-12-31
2052  581174881         GVKEYIID  10460499W  1700-01-01  2199-12-31
2053  691573602         GVKEYIID  34382202W  1700-01-01  2199-12-31
2054  691544792         GVKEYIID  34382201W  1700-01-01  2199-12-31
```

```{tip}
사용 팁: 시큐리티 마스터 검색 결과는 row-based 형식이므로 필요한 정보를 찾기 위해 검색 결과 데이터를 추가 가공해야 할 수도 있으며, 두 가지 이상의 조건을 동시에 충족하는 종목을 검색하고자 하는 경우에는 [get_securitymaster_advanced](<#get_securitymaster_advanced>) 함수를 사용하면 됩니다.
```

PrismStudio에서는 보다 편리한 시큐리티 마스터 검색을 제공하기 위하여 GUI 형태의 검색 기능을 지원하고 있습니다.

[prismstudio.securitymaster_search](<#prismstudio.securitymaster_search>) 함수를 실행하면, 아래의 그림과 같이 시큐리티 마스터를 검색할 수 있는 페이지가 나타납니다.

이 페이지에서 시큐리티 마스터 검색은 물론, 검색 결과의 각 행을 클릭하여 시간에 따른 시큐리티 마스터 attribute의 변화를 추적할 수도 있습니다.

> ***시큐리티 마스터*** ***화면***

![security-master](../_static/security-master.png)

### 데이터 아이템 검색

PrismStudio에서는 다양한 데이터를 보다 정확하게 사용할 수 있도록 각 데이터 아이템의 ID(dataitemid)를 관리하고 있으며, 이를 검색할 수 있는 [dataitems](<#prismstudio.dataitems>) 함수를 지원합니다.

올바른 데이터를 사용하기 위하여 이 기능을 활용하여 dataitemid와 데이터 분류를 적극 확인하는 것을 권장합니다.

아래 예제 코드에서는 손익계산서 내에 있는 데이터 아이템 중 순이익(Net Income) 관련 데이터를 검색합니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

# 데이터 아이템 이름에 Net Income이 들어가는 Income Statement 컴포넌트의 데이터 아이템 검색
>>> ps.financial.income_statement_dataitems("Net Income")

    dataitemid	                           dataitemname  ...             packagename
 0      100637	                  Net Income to Company  ...  CIQ Premium Financials
 1      100639	                             Net Income  ...  CIQ Premium Financials
 2      100644	        Other Adjustments to Net Income  ...  CIQ Premium Financials
 3      100645  Net Income Allocable to General Partner  ...  CIQ Premium Financials
 4      100646   Net Income to Common Incl. Extra Items  ...  CIQ Premium Financials
 5      100647   Net Income to Common Excl. Extra Items  ...  CIQ Premium Financials
 6      100703                       Diluted Net Income  ...  CIQ Premium Financials
 7      100829                               Net Income  ...  CIQ Premium Financials
 8      100830               Net Income as per SFAS 123  ...  CIQ Premium Financials
 9      100831  Net Income from Discontinued Operations  ...  CIQ Premium Financials
10	    100842                    Normalized Net Income  ...  CIQ Premium Financials
```

PrismStudio에서는 보다 편리한 데이터 아이템 검색을 제공하기 위하여 GUI 형태의 검색 기능도 지원하고 있습니다.

[prismstudio.dataitem_search](<#prismstudio.dataitem_search>) 함수를 실행하면, 아래의 그림과 같이 데이터 아이템을 검색할 수 있는 페이지가 나타납니다.

화면 좌측에서 데이터 아이템 분류(Category 및 Components)를 지정하고, 바로 우측에 검색하기 원하는 메타 데이터의 종류 및 값을 입력하여 검색할 수 있습니다.

> ***Data Items 사이트 화면***

![data-items](../_static/data-items.png)

### 쿼리, 유니버스, 포트폴리오 검색

쿼리, 유니버스, 포트폴리오 검색을 위한 함수를 지원합니다. (각각 순서대로 [prismstudio.list_dataquery](<#prismstudio.list_dataquery>), [prismstudio.list_taskquery](<#prismstudio.list_taskquery>), [prismstudio.list_universe](<#prismstudio.list_universe>), [prismstudio.list_portfolio](<#prismstudio.list_portfolio>))

아래 예제 코드처럼 함수에 파라미터로 원하는 검색어를 입력하면 해당하는 쿼리, 유니버스, 혹은 포트폴리오의 목록을 반환합니다.

이름은 경로를 나타내기도 하는데, 이와 관련한 자세한 설명은 [쿼리, 유니버스, 포트폴리오 이름과 경로](index.md)를 참고하세요.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.list_dataquery() # 모든 데이터 쿼리의 목록

   dataqueryid  dataqueryname
0	          1        myquery
1           2      roa_query
2           3      mom_query

prismstudio.list_dataquery("myquery") # 이름에 myquery를 포함한 데이터 쿼리의 목록

   dataqueryid  dataqueryname
0	           1        myquery
```

## 쿼리 작업

쿼리를 [생성하고](index.md), [저장하고](index.md), [불러오고](index.md), [변경 및 삭제하고](index.md), [업데이트](index.md) 하는 방법을 살펴보겠습니다.

### 쿼리 생성

쿼리를 생성하기 위해서는 먼저 컴포넌트를 만들어야 하며, 컴포넌트에는 아래와 같이 세 종류가 있습니다.

1. 데이터 컴포넌트
    - 데이터를 표현하기 위한 컴포넌트이며, 시장, 재무, 전망 등의 데이터셋을 지원합니다.
    - 컴포넌트로 표현할 데이터를 특정하기 위해 dataitemid를 입력할 수 있으며, dataitemid는 [데이터 아이템 검색](index.md)을 통해 찾을 수 있습니다.
2. 함수 컴포넌트
    - 기본적인 사칙연산 외에도, 횡단면 및 시계열 함수 등 금융 데이터 처리에 필요한 함수를 제공합니다.
    - 함수 컴포넌트는 데이터 컴포넌트와 PrismStudio Python Extension에서 제공하는 함수를 사용하여 생성할 수 있습니다.
3. 태스크 컴포넌트
    - 스크리닝, 팩터 백테스트, 전략 시뮬레이션 등 세 종류의 태스크를 지원하며, 태스크 컴포넌트 함수를 사용하여 생성할 수 있습니다.

전체 리스트는 [API Reference](../apiref/index.rst)에서 확인할 수 있습니다.

```{warning}
주의: 실제 컴포넌트 클래스 이름은 _PrismComponent이며, 비공개 클래스 입니다. → 클래스 생성자로 직접 객체를 만드는 것을 권장하지 않습니다.
```

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

>>> c = prismstudio.market.close() # 종가 데이터를 나타내는 컴포넌트 (데이터 컴포넌트)
>>> r = c.n_periods_pct_change(n=1) # 1일 수익률을 나타내는 컴포넌트 (함수 컴포넌트)

# 1일 수익률을 팩터 스코어로 사용한 팩터 백테스트 태스크를 나타내는 컴포넌트 (태스크 컴포넌트)
>>> fb_r = prismstudio.factor_backtest(factor=r, universe="S&P 500", frequency="Q", bins=10, startdate="2010-01-01", enddate="2015-01-01")
```

컴포넌트를 반환하거나 출력하면 컴포넌트 내부에 있는 쿼리의 요약 정보를 확인할 수 있으며, 자세한 정보는 [.query] 메서드를 통해 확인할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

>>> o = prismstudio.market.open()
>>> intraday_r = c/o

>>> print(intraday_r ) # 쿼리 출력
=== __truediv__
    ==== MarketDataComponentType.CLOSE
	  ==== MarketDataComponentType.OPEN
Query Structure

>>> intraday_r.query() # _PrismComponent().query() 메서드
==== __truediv__
	 parameters: {}
	 ==== MarketDataComponentType.CLOSE
		 parameters: {
			 package : None
			 adjustment : True
 		 currency : None
    }
	 ==== MarketDataComponentType.OPEN
 	 parameters: {
  	 package : None
			 adjustment : True
 		 currency : None
  	 }
```

태스크 컴포넌트에 대해서도 동일한 기능을 제공합니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

>>> c = prismstudio.market.close() # 종가 데이터를 나타내는 컴포넌트 (데이터 컴포넌트)

>>> r_1 = c.resample('M').n_periods_pct_change(n=1) # 1달 수익률을 나타내는 컴포넌트 (함수 컴포넌트)

>>> r_12 = c.resample('M').n_periods_pct_change(n=12) # 12달 수익률을 나타내는 컴포넌트 (함수 컴포넌트)

>>> mom = r_1 - r_12 # 12달 대비 1달 수익률 모멘텀을 나타내는 컴포넌트 (함수 컴포넌트)

>>> fb_mom = prismstudio.factor_backtest(
        factor=mom,
        universe="S&P 500",
        frequency="Q",
        bins=10,
        startdate='2010-01-01',
        enddate="2015-01-01"
        ) # factor backtest 태스크를 나타내는 컴포넌트 (태스크 컴포넌트)
```

### 쿼리 저장

컴포넌트의 [save](<#save>) 함수를 사용하면 해당 컴포넌트 내부의 쿼리를 서버에 저장할 수 있습니다.

[save_dataquery()](<#save_dataquery()>) 함수 혹은 [save_taskquery()](<#save_taskquery()>) 함수를 이용하여 같은 작업을 수행할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")
>>> c = prismstudio.market.close() # 종가 데이터를 나타내는 컴포넌트 (데이터 컴포넌트)
>>> r = c.n_periods_pct_change(n=1) # 1일 수익률을 나타내는 컴포넌트 (함수 컴포넌트)

# 아래 두 줄의 코드는 완전히 동일하게 기능합니다.
>>> r.save(dataqueryname="daily_return") # 컴포넌트 메서드를 사용하여 쿼리 저장
>>> ps.save_dataquery(component=r, dataqueryname="daily_return") # PrismStudio Extension 메서드를 사용하여 쿼리 저장
```

### 쿼리 불러오기

서버에 저장된 쿼리를 사용자의 로컬 환경으로 불러올 수 있는 기능을 제공합니다.

먼저 [list_dataquery](<#list_dataquery>)를 이용하여 이미 저장된 쿼리 목록을 확인한 후에 [load_dataquery](<#load_dataquery>)를 통해 원하는 쿼리를 불러오면 쿼리가 담긴 컴포넌트가 반환됩니다.

반환된 컴포넌트는 사용자가 직접 생성한 것과 완전히 동일하기 때문에 이를 활용해 바로 원하는 작업을 수행할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")
>>> ps.list_dataquery() # 사용자가 저장한 쿼리를 나열합니다.

>>> r = prismstudio.load_dataquery(dataquery="daily_return") # daily_return이라는 쿼리를 로컬 환경으로 불러옵니다. (쿼리가 담긴 컴포넌트를 반환합니다.)
```

### 쿼리 이름 변경 및 삭제

서버에 저장된 쿼리의 이름을 변경하거나 삭제하는 기능을 제공합니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")
>>> ps.list_dataquery() # 사용자가 저장한 쿼리를 나열합니다.

# 쿼리 이름 변경
>>> ps.rename_dataquery(old="daily_return", new="new_daily_return")

# 쿼리 삭제
>>> ps.delete_dataquery(dataquery="new_daily_return")
```

### 쿼리 업데이트

서버에 저장된 쿼리 또는 사용자의 로컬 환경에서 작업 중인 쿼리를 업데이트 하는 기능을 제공합니다.

쿼리를 생성할 때 코드를 사용했기 때문에 직접 쿼리를 수정하거나 변경하기 어려울 수 있으나, [extract](<#extract>) 함수를 활용하면 쿼리를 쉽게 업데이트할 수 있습니다.

아래 예제처럼 [extract](<#extract>) 함수는 쿼리 생성에 사용된 컴포넌트를 만들 수 있는 코드를 반환하는데, 이 코드를 업데이트하고 저장하여 쿼리를 업데이트 할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

>>> c = prismstudio.market.close() # 종가 데이터를 나타내는 컴포넌트 (데이터 컴포넌트)

>>> c.extract() # 컴포넌트를 다시 만들 수 있는 코드가 생성됩니다.
x0 = prismstudio.market.close(package="Prism Market", adjustment=None, currency=None)

# 위에서 반환된 코드를 사용하여 원하는 파라미터를 바꿀 수 있습니다.
```

## 유니버스 작업

유니버스는 종목 식별자 및 해당 종목의 유니버스 내 편입 기간 정보를 담고 있으며, 데이터 추출 시에 대상 종목을 표현하는 데 사용됩니다.

사용자는 현재 접근 권한이 있는 유니버스에 대하여 조회, 내부 데이터 조회, 신규 생성, 이름 변경, 삭제 등을 수행할 수 있습니다.

신규 유니버스를 생성하는 방법은 크게 세 가지가 있으며 이는, [1) 인덱스 활용](index.md), [2) 유니버스 필터](index.md), [3) 스크린 태스크 활용](index.md)입니다.

### 인덱스 활용

[prismstudio.save_index_as_universe](<#prismstudio.save_index_as_universe>) 메서드를 이용하여 인덱스를 유니버스로 저장하는 방식으로 유니버스를 생성할 수 있습니다.

이 메서드에는 파라미터로 dataitemid를 입력할 수 있으며, 각 인덱스의 dataitemid는 [prismstudio.index.dataitems](<#prismstudio.index.dataitems>)를 이용하여 검색할 수 있습니다.

단, [prismstudio.index.dataitems](<#prismstudio.index.dataitems>)는 모든 인덱스를 대상으로 검색하기 때문에 유니버스 생성이 가능한 인덱스만 검색하려면 [prismstudio.index.universe_dataitems](<#prismstudio.index.universe_dataitems>)를 이용하면 됩니다.

물론 [데이터 아이템 검색 GUI 페이지](index.md)를 활용하여 검색할 수도 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")
>>> ps.index.universe_dataitems("S&P 500") # "S&P 500"을 포함하고, 유니버스에 사용할 수 있는 인덱스 데이터 아이템을 나열합니다.

# 4006682번 인덱스(S&P 500)를 유니버스 'my_snp_500'으로 저장합니다.
>>> ps.save_index_as_universe(dataitemid=4006682, startdate='2020-01-01', enddate='2021-01-01', universename='my_snp_500')
>>> ps.list_universe() # 사용자가 저장한 유니버스의 목록을 가져옵니다.
```

### 유니버스 필터

시큐리티 마스터의 attribute를 기준으로 전체 종목을 필터하여 유니버스를 생성할 수 있습니다.

특히 시큐리티 마스터의 attribute 중 메타 데이터를 이용한다면 보다 높은 자유도를 가지고 초기 유니버스를 구성할 수 있습니다.

아래 예제와 같이 [prismstudio.filter_universe](<#prismstudio.filter_universe>)를 이용하여 필터할 수 있으며, 한 종류의 attribute에만 필터 조건을 적용할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

# 한국과 미국 주식을 모두 담은 유니버스를 만듭니다. Korea and US 라는 이름의 유니버스가 만들어집니다.
>>> ps.filter_universe(attribute="Country", value=["KR", "US"], universename="Korea and US")
```

더 복잡한 규칙을 이용하여 유니버스를 생성하기 원한다면 [스크린 태스크 활용](index.md)을 참고하세요.

### 유니버스 추출

[prismstudio.get_universe](<#prismstudio.get_universe>)에 유니버스 이름 또는 ID를 입력하여 생성된 유니버스 데이터를 추출할 수 있습니다.

이 함수는 기본적으로 구성 종목의 변경점을 기준으로 유니버스 데이터를 반환하며, 만약 expand=True 파라미터를 추가하면 일 단위 주기로 조정된 데이터를 반환합니다.

유니버스 추출 결과에 해당 종목의 메타 데이터를 추가하기 원한다면 shownid 파라미터를 사용할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")
>>> ps.list_universe() # 사용자가 저장한 유니버스의 목록을 불러옵니다.

>>> ps.get_universe("S&P 500", shownid=["Company Name", "Ticker"]) # S&P 500 유니버스 구성 종목과 그 회사명 및 티커를 불러옵니다.
        listingid        date                  Company Name  Ticker
     0    2586210  1964-03-31           MULTIGRAPHICS, INC.      AM
     1    2586222  1964-03-31  AMERICAN AIRLINES GROUP INC.     AMR
     2    2586324  1964-03-31                    AT&T CORP.       T
     3    2586533  1964-03-31           ABBOTT LABORATORIES     ABT
     4    2587301  1964-03-31        AEROQUIP-VICKERS, INC.     ANV
   ...        ...         ...                           ...     ...
799592  658545221  2199-12-31    OTIS WORLDWIDE CORPORATION    OTIS
799593  658545324  2199-12-31    CARRIER GLOBAL CORPORATION    CARR
799594  677853450  2199-12-31    CAESARS ENTERTAINMENT, INC.    CZR
799595  678367691  2199-12-31                   VIATRIS INC.   VTRS
799596  706171023  2199-12-31                APA CORPORATION    APA
```

### 유니버스 이름 변경 및 삭제

서버에 저장된 유니버스에 대하여 그 이름을 변경하거나 삭제할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")
>>> ps.list_universe() # 사용자가 저장한 유니버스의 목록을 불러옵니다.

# 유니버스 이름 변경
>>> ps.rename_universe(old="S&P 500", new="New S&P 500")

# 유니버스 삭제
>>> ps.delete_universe(universe="New S&P 500")
```

## 포트폴리오 작업

포트폴리오는 두 가지 데이터로 구성되며, 이는 각각 포트폴리오 밸류와 포트폴리오 레벨입니다.

포트폴리오 밸류는 구성 종목의 주식 수를 말하며, 포트폴리오 레벨은 아래의 7가지 시계열 정보를 말합니다.

- Total Return Gross
- Price Return
- Currency Hedged Return
- Total Return Net
- Currency Hedged Total Return Gross
- Currency Hedged Total Return Net
- Volatility

사용자는 현재 접근 권한이 있는 포트폴리오에 대하여 조회, 내부 데이터 조회, 신규 생성, 이름 변경, 삭제 등을 수행할 수 있습니다.

신규 포트폴리오를 생성하는 법은 크게 두 가지가 있으며 이는, [1) 인덱스 활용](index.md), 2) 전략 시뮬레이션 태스크 활용입니다.

### 인덱스 활용

[prismstudio.save_index_as_portfolio](<#prismstudio.save_index_as_portfolio>) 메서드를 이용하여 인덱스를 포트폴리오로 저장하는 방식으로 포트폴리오를 생성할 수 있습니다.

이 메서드에는 파라미터로 dataitemid를 입력할 수 있으며, 각 인덱스의 dataitemid는 [prismstudio.index.dataitems](<#prismstudio.index.dataitems>)를 이용하여 검색할 수 있습니다.

단, [prismstudio.index.dataitems](<#prismstudio.index.dataitems>)는 모든 인덱스를 대상으로 검색하기 때문에 포트폴리오 생성이 가능한 인덱스만 검색하려면 [prismstudio.index.portfolio_dataitems](<#prismstudio.index.portfolio_dataitems>)를 이용하면 됩니다.

물론 [데이터 아이템 검색 GUI 페이지](index.md)를 활용하여 검색할 수도 있습니다.

```{warning}
주의:  위에서 언급한 포트폴리오를 구성하는 두 가지 데이터를 모두 얻을 수 있는 인덱스만 포트폴리오로 저장할 수 있습니다.
```

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")
>>> ps.index.portfolio_dataitems("S&P 500") # "S&P 500"을 포함하고, 포트폴리오에 사용할 수 있는 인덱스 데이터 아이템을 나열합니다.

# 4006682번 인덱스(S&P 500)를 포트폴리오 'my_snp_500_ppt'으로 저장합니다.
>>> ps.save_index_as_portfolio(dataitemid=4006682, startdate='2020-01-01', enddate='2021-01-01', universename='my_snp_500_ppt')
>>> ps.list_portfolio() # 사용자가 저장한 유니버스의 목록을 불러옵니다.
```

### 포트폴리오 추출

[prismstudio.get_portfolio](<#prismstudio.get_portfolio>)에 포트폴리오 이름 또는 ID를 입력하여 생성된 포트폴리오 데이터를 추출할 수 있으며, 포트폴리오를 구성하는 두 가지 데이터가 반환됩니다.

포트폴리오 추출 결과에 해당 종목의 메타 데이터를 추가하기 원한다면 shownid 파라미터를 사용할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")
>>> ps.list_portfolio() # 사용자가 저장한 포트폴리오의 목록을 불러옵니다.

# S&P 500 포트폴리오의 레벨, 구성 종목과 주식 수, 회사명 및 티커를 불러옵니다.
>>> ps.get_portfolio("S&P 500", shownid=["Company Name", "Ticker"])
```

### 포트폴리오 이름 변경 및 삭제

서버에 저장된 포트폴리오에 대하여 그 이름을 변경하거나 삭제할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")
>>> ps.list_portfolio() # 사용자가 저장한 포트폴리오의 목록을 불러옵니다.

# 포트폴리오 이름 변경
>>> ps.rename_portfolio(old="S&P 500", new="New S&P 500")

# 포트폴리오 삭제
>>> ps.delete_portfolio(portfolio="New S&P 500")
```

## 데이터 작업

### 데이터 추출

쿼리는 처리할 데이터 종류와 수행할 연산 정보만 가지고 있을 뿐 데이터를 저장하고 있지 않습니다.

따라서 데이터(혹은 쿼리에 의해 연산된 결과 데이터)를 불러오고 싶다면 [get_data](<#prismstudio.get_data>)를 활용해 데이터를 추출해야 합니다.

[get_data](<#prismstudio.get_data>)에 컴포넌트, 유니버스 및 데이터 기간 등을 입력하면 Pandas DataFrame 형태로 데이터를 추출할 수 있습니다.

여러 컴포넌트를 리스트 형태로 입력하여 동시에 여러 데이터를 추출할 수도 있으며 이 때에는 컴포넌트 입력 순서에 따라 데이터가 반환됩니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")
>>> c = prismstudio.market.price_close() # 종가 데이터를 나타내는 컴포넌트 (데이터 컴포넌트)
>>> r = c.n_periods_pct_change(n=1) # 1일 수익률을 나타내는 컴포넌트 (함수 컴포넌트)

# my_snp_500 유니버스에서 2020-01-01과 2020-12-31 사이 r 컴포넌트에 해당하는 데이터를 종목의 회사 이름, ISIN코드와 함께 daily_return이라는 이름으로 불러옵니다.
>>> r.get_data(universe='my_snp_500', startdate='2020-01-01', enddate='2020-12-31', name=["daily_return"], shownid=['Company Name', 'ISIN'])

# 위와 같은 설정에서 c과 r에 해당하는 데이터를 close과 daily_return이라는 이름으로 불러옵니다.
>>> ps.get_data(
        component=[c, r],
        universe='my_snp_500',
        startdate='2020-01-01',
        enddate='2020-12-31',
        name=["close", "daily_return"],
        shownid=['Company Name', 'ISIN']
        )
```

```{warning}
주의: 날짜 파라미터는 Python datetime 모듈 기본 설정 기준을 따르는 형식이어야 하며, 시작일과 종료일을 모두 입력해야 합니다.
```

### 데이터 보기

PrismStudio에서는 아래 그림과 같은 자체 데이터 조회 기능을 지원하고 있으며, 컴포넌트에서 [view_data](<#prismstudio.view_data>) 함수를 호출하면 Data Viewer 사이트로 연결됩니다.

이 기능을 활용하면 마우스를 이용하여 간단하고 빠르게 데이터를 정렬하거나 필터 할 수 있고 한 눈에 데이터를 파악할 수 있습니다.

> ***Data Viewer 사이트 화면***

![data-viewer](../_static/data-viewer.png)

---

# **🗄 태스크**

PrismStudio에서는 [스크린](index.md), [팩터 백테스트](index.md), 전략 시뮬레이션 3개의 태스크를 지원하며, 각 태스크에 대한 세부 설명은 [API Reference](../apiref/index.rst)에서 확인할 수 있습니다.

태스크를 실행하기 위해서는 다음의 두 작업을 수행해야 합니다.

1. 태스크 컴포넌트 생성
    - [prismstudio.factor_backtest](<#prismstudio.factor_backtest>)와 같은 함수를 사용하여 태스크 컴포넌트를 생성합니다.
    - 태스크 컴포넌트는 데이터 컴포넌트와 마찬가지로 저장할 수 있습니다.
2. 태스크 실행
    - 태스크 컴포넌트에서 run 메서드([screen.run](<#screen.run>), [prismstudio.factor_backtest.run](<#prismstudio.factor_backtest.run>) 등)를 사용하여 태스크를 실행할 수 있습니다.

태스크가 실행되면 job으로 기록되며, 사용자가 따로 설정하지 않는 경우 job의 이름은 [태스크 타입]_[jobid]으로 저장됩니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

>>> ni = prismstudio.financial.income_statement(100639, periodtype="LTM") # 100639: Net Income을 나타내는 컴포넌트 (데이터 컴포넌트)
>>> ta = prismstudio.financial.balance_sheet(100033, periodtype="Q") # 100033: Total Assets를 나타내는 컴포넌트 (데이터 컴포넌트)
>>> roa = ni/ta # ROA를 나타내는 컴포넌트 (함수 컴포넌트)

# 태스크 컴포넌트를 생성합니다.
>>> roa_fb = prismstudio.factor_backtest(factor=roa, universe="S&P 500", frequency="Q", bins=10, startdate="2010-01-01", enddate="2015-01-01")

# 태스크를 실행 합니다.
>>> roa_fb.run()
```

## 스크린

스크린 태스크를 통해 특정한 조건을 충족하는 종목을 선별하고 유니버스로 저장할 수 있으며, 흔히 종목 스크리닝이라고 부르기도 합니다.

이 태스크에서는 종목 선별 조건을 불리언(boolean)의 형태로 표현하는 컴포넌트를 이용해 그 값이 참인 종목만 유니버스에 편입합니다.

```{tip}
사용 팁: 불리언 연산 컴포넌트를 사용하거나, map함수를 사용해 불리언 데이터 쿼리를 만들 수 있습니다.
```

아래 예제에서는 한국거래소에서 거래되는 종목 중 CIQ Primary 종목에 대해 금융 섹터를 제외하고 시가총액 상위 200개에 속하는 종목을 신규 유니버스로 저장합니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

>>> primary_rule = prismstudio.securitymaster.attribute(attribute="CIQ Primary") == "primary" # CIQ Primary 종목만 포함합니다.
>>> non_financial_rule = prismstudio.securitymaster.attribute(attribute="GICS Sector") != "40" # 금융 섹터를 포함하지 않습니다.
>>> mcap = prismstudio.market.market_cap()
>>> marketcap_rule = mcap.cross_sectional_rank() <= 200 # 주어진 날짜에 시가총액 상위 200개를 포함합니다.

# 위 세 개의 규칙을 적용하여 스크린 태스크 컴포넌트를 생성합니다.
>>> krx_200_screen = prismstudio.screen(
        rule=primary_rule & non_financial_rule & marketcap_rule, # 세 룰을 모두 적용합니다.
        universename="krx", # 기존 유니버스는 이미 만들어진 krx 유니버스 입니다.
        startdate="2010-01-01",
        enddate="2015-01-01",
        frequency="D",
        )

# 스크린 된 유니버스를 저장할 이름을 명시하여 태스크를 실행합니다.
>>> krx_200_screen.run(newuniversename="krx_primary_top200_nonfinancial")
```

스크린을 통해 유니버스를 생성한 후에는 [prismstudio.list_universe](<#prismstudio.list_universe>)를 실행하여 생성된 유니버스를 확인할 수 있습니다.

전체 종목으로부터 유니버스를 생성하는 기능은 [유니버스 필터](<#prismstudio.filter_universe>)를 참고하세요.

## 팩터 백테스트

팩터 백테스트는 팩터의 투자 효용성을 평가할 수 있는 태스크이며, 사용자는 손 쉽게 다양한 팩터의 예측력을 실험할 수 있습니다.

아래 예제에서는 총 매출 및 시가 총액 데이터를 이용하여 Sales to Price 팩터를 생성하고 이를 백테스트 합니다.

1. 총 매출 데이터를 표현하는 컴포넌트를 [prismstudio.financial.income_statement](<#prismstudio.financial.income_statement>) 함수를 이용하여 생성합니다. 데이터 주기는 LTM으로, 통화 종류는 거래 기준으로 설정합니다.

    ```python
    >>> import prism

    >>> ps.login(username="my_username", password="my_password")

    >>> rev = prismstudio.financial.income_statement(100589, periodtype='LTM', currency='trade') # 100589: Revenue, Total(총 매출)을 표현하는 컴포넌트 (데이터 컴포넌트)
    ```


1. 시가 총액 데이터를 표현하는 컴포넌트를 [prismstudio.market.market_cap](<#prismstudio.market.market_cap>) 함수를 이용하여 생성합니다.

    ```python
    >>> mcap = prismstudio.market.market_cap() # 시가 총액을 표현하는 컴포넌트 (데이터 컴포넌트)
    ```


1. 총 매출 데이터의 주기는 분기이고, 시가 총액 데이터의 주기는 매일이므로, 총 매출 데이터를 매일 주기로 리샘플링 합니다.

    ```python
    >>> rev = rev.resample('D')
    ```


1. 총 매출과 시가 총액을 나누어 sp로 저장합니다.

    ```python
    >>> sp = rev / mcap
    ```


1. [prismstudio.factor_backtest](<#prismstudio.factor_backtest>) 함수를 이용하여 S&P 500 유니버스에 대해 Sales to Price 팩터를 백테스트 합니다. 퀀타일의 수(bins)는 5, 재조정 주기(frequency)는 월(’M’), 백테스트 기간은 2016-12-31 ~ 2020-01-01으로 설정하고, 태스크 컴포넌트를 sp_fb에 저장한 후 실행합니다.

    ```{warning}
    주의: 결과에서 보이는 Bin 1(1번 퀀타일)은 팩터의 값이 높은 주식이 포함된 퀀타일 입니다.
    ```

    ```python
    # 태스크 컴포넌트
    >>> sp_fb = prismstudio.factor_backtest(factor=sp, universe="S&P 500", frequency="M", bins=5, startdate='2016-12-31', enddate='2020-01-01')
    # 태스크 실행
    >>> sp_fb.run()
    ```


1. 팩터 백테스트가 완료되면 리포트가 생성되고, 브라우저의 새 탭에 열립니다.

> ***팩터 백테스트 리포트 화면***

[factor_backtest_report.mp4](../_static/factor_backtest_report.mp4)

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

>>> rev = prismstudio.financial.income_statement(100589, periodtype='LTM', currency='trade') # 100589: Revenue, Total(총 매출)을 표현하는 컴포넌트 (데이터 컴포넌트)
>>> mcap = prismstudio.market.market_cap() # 시가 총액을 표현하는 컴포넌트 (데이터 컴포넌트)
>>> rev = rev.resample('D')
>>> sp = rev / mcap

# 태스크 컴포넌트
>>> sp_fb = prismstudio.factor_backtest(factor=sp, universe="S&P 500", frequency="M", bins=10, startdate='2016-12-31', enddate='2020-01-01')
# 태스크 실행
>>> sp_fb.run()
```

## Job 작업

태스크를 실행할 때마다 하나의 job이 생성되고 그 태스크 및 그 실행 정보 및 결과가 기록됩니다.

사용자는 아래 그림의 [Job Manager 사이트](index.md)에서 job을 관리 및 확인할 수 있고, 그 데이터를 받아볼 수 있습니다.

> ***Job Manager 사이트 화면***
>

![job-manager](../_static/job-manager.png)

### Job 검색

쿼리나 유니버스, 포트폴리오와 같이 job 또한 [list_job](<#list_job>) 메서드를 통해서 검색할 수 있습니다.

Job의 세부 정보는 [get_job](<#get_job>) 메서드를 통해 확인할 수 있으며, 태스크 종류별로 정보를 확인하고자 한다면 [prismstudio.screen_jobs](<#prismstudio.screen_jobs>), [prismstudio.factor_backtest_jobs](<#prismstudio.factor_backtest_jobs>) 메서드를 사용할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

# 2021년 11월 01일과 2021년 10월 01일 사이에 성공적으로 실행된 스크린 태스크 실행 job 히스토리를 가져옵니다.
>>> ps.list_jobs(jobstatus='Completed', taskquerytype='screen', startrange='2021-10-01', endrange='2021-11-01')

>>> ps.get_job(jobid=1)

>>> ps.screen_jobs()
>>> ps.factor_backtest_jobs()
>>> ps.strategy_backtest_jobs()
```

### Job 결과 데이터 추출

팩터 백테스트와 전략 시뮬레이션 태스크의 경우에는 job의 결과를 [prismstudio.factor_backtest.get_result](<#prismstudio.factor_backtest.get_result>) 메서드를 이용하여 데이터 형태로 추출할 수 있습니다.

성공적으로 실행되어 결과가 기록된 팩터 백테스트와 전략 시뮬레이션 태스크에는 job id 이외에 각각 fbid와 sbid가 부여되고, job 검색을 통해 확인할 수 있습니다.

```{warning}
결과 데이터를 가져오기 위해서는 job id가 아닌 fbid(factor backtest id) 또는 sbid(strategy backtest id)를 사용해야 합니다.
```

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

# 팩터 백테스트 결과를 데이터로 추출합니다.
>>> ps.factor_backtest.get_result(fbid=1)
{'ar':    Top-Bottom Spread     Bin 1     Bin 2     Bin 3     Bin 4     Bin 5
    0          -0.000486  0.001492  0.001504  0.001152  0.000494  0.000786,
    'counts':          date  Bin 1  Bin 2  Bin 3  Bin 4  Bin 5
    0  2017-01-31     34     35     34     35     35
    1  2017-02-28     90     90     90     90     90
    2  2017-03-31     93     93     94     93     94
  ...         ...    ...    ...    ...    ...    ...
   35  2019-12-31     93     94     93     94     94,
    'ic':          date        ic
    0  2017-01-31  0.064979
    1  2017-02-28 -0.183307
    2  2017-03-31 -0.173303
  ...         ...       ...
   34 2019-11-30  0.083536,
    'pnl':          date  Top-Bottom Spread     Bin 1     Bin 2     Bin 3     Bin 4  \
    0  2017-01-31           0.002140  0.017746  0.043898  0.036038  0.037294
    1  2017-02-28          -0.021081  0.026620  0.051022  0.033684  0.038632
    2  2017-03-31          -0.049464  0.044036  0.060882  0.037305  0.049272
  ...         ...                ...       ...       ...       ...       ...
   34 2019-11-30          -0.145846  0.448767  0.452153  0.346276  0.148477

          Bin 5
   0   0.019886
   1   0.005146
   2  -0.006945
 ...        ...
  34   0.236161,
   ...}
```

### Job 이름/설명 변경 및 삭제

모든 job에 대하여 설명을 추가할 수 있고, 이름을 변경하거나 삭제할 수 있습니다.

[Job Manager 사이트](index.md)에서 원하는 job의 행을 클릭하면 나타나는 오른쪽 패널에서 job의 이름을 변경하거나 설명을 추가하거나 삭제할 수 있습니다.

단, job을 삭제하면 결과 리포트는 삭제되지만 결과로 생성된 유니버스나 포트폴리오는 삭제되지 않습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

>>> ps.rename_job(jobid=1, jobname="my_jobname") # jobid 1에 해당하는 잡의 이름을 my_jobname으로 설정합니다.

>>> ps.add_job_description(jobid=1, description="this is my job") # jobid 1에 해당하는 잡에 this is my job이라는 설명을 추가합니다.
```

### Job 코드 추출

Job이 생성될 당시의 태스크 컴포넌트를 생성하기 위한 코드를 [prismstudio.extract_job](<#prismstudio.extract_job>)을 이용하여 자동으로 만들 수 있습니다.

[Job Manager 사이트](index.md)에서 원하는 job의 행을 클릭하면 나타나는 오른쪽 패널에서 Extract 버튼을 클릭하여 코드를 확인할 수 있습니다.

코드의 파라미터를 업데이트하면 동일한 태스크를 여러 가지 설정으로 실행할 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.login(username="my_username", password="my_password")

>>> ni = prismstudio.financial.income_statement(100639, periodtype="LTM") # 100639: Net Income을 나타내는 컴포넌트 (데이터 컴포넌트)
>>> mcap = prismstudio.market.market_cap() # 시가총액을 나타내는 컴포넌트 (데이터 컴포넌트)
>>> ep = ni / mcap # E/P를 나타내는 컴포넌트 (함수 컴포넌트)
>>> ep_fb = prismstudio.factor_backtest(factor=ep, universe="S&P 500", startdate="2013-01-01", enddate="2015-01-01", frequency="Q", bins=10)
>>> ep_fb.run()
Done!
factor_backtest Completed: factorbacktestid is 1
Fetching A Link to Factor Backtest Report...
Link to Factor Backtest Report:
https://ext.prism39.com/report/factor_backtest/my_username_1_96cebcc1-fe3d-4de7-b433-e32d6fcc13c9/

>>> ps.extract_job(jobid=1) # 위에서 실행한 job(jobid = 1)을 실행할 때 사용한 태스크 컴포넌트를 만드는 코드를 생성합니다.
x0 = prismstudio.financial.income_statement(dataitemid=100639, periodtype="LTM", package="CIQ Premium Financials", preliminary=True, currency=None)
x1 = prismstudio.market.marketcap(currency=None, package="CIQ Market")
x2 = x0 / x1
x3 = prismstudio.factor_backtest(factor_dataquery=x2, universeid=2, startdate="2013-01-01", enddate="2015-01-01", frequency="Q", bins=10, rank_method="standard", max_days=None)

# 위에서 반환된 코드를 사용하여 원하는 파라미터를 바꿀 수 있습니다.
```

---

# 🔗 쿼리, 유니버스, 포트폴리오 이름 및 경로

## 이름 및 경로 설정

쿼리(데이터 쿼리, 태스크 쿼리), 유니버스, 포트폴리오는 이름이 경로(폴더 구조)를 나타냅니다. 폴더 구별자는 ‘/’(forward slash)입니다. 제일 마지막 ‘/’ 뒤에 오는 이름이 쿼리, 유니버스, 포트폴리오의 이름이 되고 그 앞은 폴더를 나타냅니다. 예를 들어, 데이터 쿼리를 저장할 때 ‘myfolder/myquery’를 dataqueryname으로 설정했다면, myfolder는 폴더를, myquery는 데이터 쿼리 이름을 나타냅니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> c = prismstudio.market.close() # 종가 데이터를 나타내는 컴포넌트 (데이터 컴포넌트)
>>> r = c.n_periods_pct_change(n=1) # 1일 수익률을 나타내는 컴포넌트 (함수 컴포넌트)
>>> r.save("myfolder/myquery") # myfolder는 폴더, myquery는 쿼리 이름
```

쿼리, 유니버스, 포트폴리오 모두에서 같은 규칙이 적용되며, [list_dataquery](<#list_dataquery>)를 이용하면 아래와 같이 폴더 구조를 시각적으로 볼 수 있습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.list_dataquery(tree=True) # 데이터 쿼리의 폴더 구조 시각화
dataquery/
├── roa_query
├── myfolder/
│   ├── myquery
│   └── testquery
└── high_mom_query
```

## 이름 및 경로 변경

유니버스, 포트폴리오, 쿼리의 이름을 변경할 수 있습니다. 단, 변경한 이름 또한 위 규칙에 따라 새로운 폴더로 이동할 수 있다는 점을 주의해야 합니다. 위의 예시에서 myquery를 myfolder 밖으로 꺼내면 아래와 같습니다.

```{note}
예제 코드 (Self-Contained: 그대로 실행 가능한 코드입니다.)
```

```python
>>> import prism

>>> ps.rename_dataquery(old="myfolder/myquery", new="myquery") # myfolder/myquery 쿼리 이름을 myquery로 변경
>>> ps.list_dataquery(tree=True) # 데이터 쿼리의 폴더 구조 시각화
dataquery/
├── roa_query
├── myfolder/
│   └── testquery
├── myquery
└── high_mom_query
```

---

# 부록: PrismStudio 자료구조

PrismStudio Python Extension은 PrismStudio 서버와 소통하기 위해 [컴포넌트](index.md)와 [쿼리](index.md)라는 자료구조를 사용합니다.

실제로 컴포넌트만을 사용하여 모든 기능을 사용할 것이기 때문에 컴포넌트를 먼저 이해하는 것이 좋습니다.

## 컴포넌트

컴포넌트는 데이터나 데이터 연산을 나타내는 자료구조로, **[데이터컴포넌트](index.md), [함수컴포넌트](index.md)**, 그리고 [태스크컴포넌트](index.md)로 나누어집니다.

컴포넌트는 간단한 함수를 사용하여 만들 수 있으며, [쿼리 생성](index.md)에서 자세히 다룹니다.

***데이터컴포넌트**는 데이터의 종류를 나타내는 자료구조이며 “데이터 추출 명령”을 표현합니다.

- PrismStudio는 가격, 시가총액, 재무, 인덱스 등 사용자가 접근 권한이 있는 모든 데이터의 추출과 연산을 지원합니다.

```{tip}
사용 팁: 성격이 같은 데이터컴포넌트를 접근하기 쉽게 묶어놓은 그룹을 카테고리(category)이라고 합니다. 시장(market), 재무(financial), 추정치(estimate) 등의 카테고리가 있습니다.
```

***함수컴포넌트**는 연산을 나타내는 자료구조이며 “데이터 가공 명령”을 표현합니다.

- 여타 컴포넌트에 간단한 함수를 적용하는 것으로 함수컴포넌트를 만들 수 있습니다. (함수 컴포넌트 함수의 결과는 컴포넌트입니다.)
- 프리즘스튜디오는 사칙연산을 포함하여 종단면, 횡단면 연산까지 다양한 시계열 연산을 지원합니다.
특히, 간단한 연산(사칙연산, 지수함수 등)은 파이썬 네이티브 연산 문법을 곧바로 사용할 수 있습니다.

***태스크컴포넌트**는 태스크 설정을 나타내는 자료구조이며 “태스크 실행 명령”을 표현합니다.

- 프리즘스튜디오 파이썬 익스텐션 최상단에서 접근 가능한 태스크를 사용하여 만들 수 있습니다.
- 태스크 컴포넌트에서 .run()을 실행하면 태스크를 실제로 실행 할 수 있습니다.

## 쿼리

쿼리는 순차적인 데이터 관련 명령을 표현하는 자료구조이며, 컴포넌트 없이는 생존이 불가능합니다.

쿼리는 모든 컴포넌트 안에 존재하며, 각 컴포넌트가 만들어지기까지의 과정을 담고 있습니다.

쿼리는 재사용이 가능합니다. 즉, 쿼리를 저장하고 불러올 수 있습니다.

```{warning}
주의: 쿼리는 데이터를 담고 있지 않습니다. 데이터 종류와 연산에 관한 정보만을 담고 있습니다.
```
