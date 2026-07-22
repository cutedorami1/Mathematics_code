# Engineering CAS Calculator

Python과 SymPy를 이용해 제작한 공학수학용 GUI 계산기입니다.

미분, 적분, 라플라스 변환, Z 변환, 푸리에 변환, 방정식, 행렬 및 함수 그래프 등의 계산을 하나의 GUI 환경에서 수행할 수 있습니다.

## 주요 기능

### 미적분

* 미분 및 고계 미분
* 부정적분
* 정적분
* 극한
* 테일러 급수

### 신호 및 시스템

* 라플라스 변환
* 역라플라스 변환
* 단측 Z 변환
* 역 Z 변환 계수 계산
* 푸리에 변환
* 역푸리에 변환

### 대수 계산

* 대수식 단순화
* 인수분해
* 식 전개
* 부분분수 전개
* 방정식 풀이
* 연립방정식 풀이

### 공업수학

* 1계 상미분방정식 풀이
* 행렬식 계산
* 역행렬 계산
* 전치행렬 계산
* 고유값 계산
* 행렬의 계수 계산
* 행렬 덧셈 및 곱셈

### 그래프

* 단일 함수 그래프
* 여러 함수 동시 출력
* 그래프 확대 및 이동
* 그래프 이미지 저장

## 개발 환경

* Python 3
* tkinter
* SymPy
* NumPy
* Matplotlib

Python 3.10 이상의 환경을 권장합니다.

### 1. Python 설치 확인

Windows 명령 프롬프트 또는 VS Code 터미널에서 다음 명령어를 입력합니다.

```bash
python --version
```

환경에 따라 다음 명령어를 사용해야 할 수도 있습니다.

```bash
py --version
```

Python 버전이 표시되지 않는다면 Python을 먼저 설치해야 합니다.

### 2. 설치해야하는 라이브러리

Python 3.10 이상
SymPy         
NumPy          
Matplotlib  
tkinter   

### 3. pip 업그레이드

```bash
python -m pip install --upgrade pip
```

Windows에서 `python` 명령어가 동작하지 않고 `py`가 동작한다면 다음과 같이 입력합니다.

```bash
py -m pip install --upgrade pip
```

### 4. 필요한 라이브러리 설치

```bash
python -m pip install -r requirements.txt
```

또는 라이브러리를 직접 설치할 수 있습니다.

```bash
python -m pip install sympy numpy matplotlib
```

Windows에서 `py` 명령어를 사용하는 경우:

```bash
py -m pip install sympy numpy matplotlib
```

## 실행 방법

프로그램 파일이 있는 폴더에서 다음 명령어를 입력합니다.

```bash
python engineering_cas_gui.py
```

Windows 환경에서 `py` 명령어를 사용하는 경우:

```bash
py engineering_cas_gui.py
```

VS Code에서는 `engineering_cas_gui.py` 파일을 연 뒤 오른쪽 위의 실행 버튼을 눌러 실행할 수도 있습니다.

## tkinter 확인 방법

프로그램 창이 열리지 않거나 tkinter 관련 오류가 발생하면 다음 명령어를 실행합니다.

```bash
python -m tkinter
```

작은 테스트 창이 나타나면 tkinter가 정상적으로 설치된 것입니다.

Linux Ubuntu 환경에서는 tkinter를 별도로 설치해야 할 수 있습니다.

```bash
sudo apt update
sudo apt install python3-tk
```

## 사용 방법

1. 프로그램을 실행합니다.
2. 왼쪽 위에서 원하는 연산을 선택합니다.
3. 수식 입력란에 계산할 식을 입력합니다.
4. 변수, 차수, 범위 등의 조건을 설정합니다.
5. `계산` 버튼을 누릅니다.
6. 오른쪽 계산 결과 탭에서 결과를 확인합니다.

다음 단축키로도 계산할 수 있습니다.

```text
Ctrl + Enter
F5
```

## 수식 입력 규칙

수식은 Python 및 SymPy 형식으로 입력합니다.

### 곱셈

곱셈 기호 `*`를 반드시 입력해야 합니다.

```text
2*x
x*sin(x)
3*exp(-2*t)
```

다음과 같이 입력하면 안 됩니다.

```text
2x
xsin(x)
```

### 거듭제곱

```text
x**2
t**3
```

`x^2` 형식도 프로그램 내부에서 `x**2`로 변환됩니다.

### 주요 함수

```text
sin(x)
cos(x)
tan(x)
exp(x)
sqrt(x)
log(x)
abs(x)
```

### 주요 상수

```text
pi
E
I
oo
```

* `pi`: 원주율
* `E`: 자연상수
* `I`: 허수 단위
* `oo`: 무한대

공학에서 사용하는 허수 단위 `j`도 입력할 수 있습니다.

## 사용 예시

### 미분

연산: `미분`

```text
exp(-2*x)*sin(3*x)
```

변수:

```text
x
```

미분 차수:

```text
1
```

### 정적분

연산: `정적분`

```text
sin(x)
```

설정:

```text
적분 변수: x
하한: 0
상한: pi
```

### 라플라스 변환

연산: `라플라스 변환`

```text
exp(-2*t)*sin(3*t)
```

설정:

```text
시간 변수: t
복소 변수: s
```

### 역라플라스 변환

연산: `역라플라스 변환`

```text
1/(s**2 + 4)
```

설정:

```text
복소 변수: s
시간 변수: t
```

### Z 변환

연산: `Z 변환`

```text
(1/2)**n
```

설정:

```text
이산 변수: n
Z 변수: z
시작 n: 0
```

### 역 Z 변환

연산: `역 Z 변환`

```text
z/(z - 1/2)
```

설정:

```text
Z 변수: z
이산 변수: n
계열 차수: 10
```

### 푸리에 변환

연산: `푸리에 변환`

```text
exp(-t**2)
```

설정:

```text
시간 변수: t
주파수 변수: w
```

### 부분분수 전개

연산: `부분분수`

```text
(2*s + 3)/(s*(s + 1))
```

변수:

```text
s
```

### 방정식 풀이

연산: `방정식 풀기`

```text
x**2 - 5*x + 6 = 0
```

변수:

```text
x
```

### 연립방정식

연산: `연립방정식`

```text
x + 2*y = 5; 3*x - y = 4
```

변수:

```text
x,y
```

여러 방정식은 세미콜론 `;`으로 구분합니다.

### 미분방정식

연산: `1계 미분방정식`

```text
Derivative(y(x), x) + y(x) = exp(x)
```

독립 변수:

```text
x
```

### 행렬식

연산: `행렬 계산`

```text
[[1, 2], [3, 4]]
```

행렬 연산:

```text
det
```

사용 가능한 행렬 연산은 다음과 같습니다.

```text
det
inv
transpose
eigen
rank
add
multiply
```

### 함수 그래프

연산: `함수 그래프`

```text
sin(x); cos(x); exp(-0.2*x)*sin(3*x)
```

여러 함수는 세미콜론 `;`으로 구분합니다.

그래프 설정 예시:

```text
변수: x
최솟값: -10
최댓값: 10
점 개수: 1000
```

## 프로젝트 파일 구성

```text
Engineering-CAS/
├── engineering_cas_gui.py
├── requirements.txt
└── README.md
```

* `engineering_cas_gui.py`: 프로그램의 메인 소스 코드
* `requirements.txt`: 필요한 Python 라이브러리 목록
* `README.md`: 프로그램 설명 및 실행 방법

## 주의사항

### Z 변환

현재 Z 변환 기능은 다음과 같은 단측 Z 변환 정의를 사용합니다.

```text
X(z) = Σ x[n]z^(-n)
```

합은 사용자가 입력한 시작값부터 무한대까지 계산됩니다.

기본 시작값은 다음과 같습니다.

```text
n = 0
```

### 역 Z 변환

역 Z 변환은 `z = ∞`, 즉 `z^(-1) = 0` 부근의 급수 전개를 이용해 수열 계수를 계산합니다.

따라서 기본적으로 인과 수열을 대상으로 하며, 수렴영역에 따른 좌측 수열이나 양측 수열을 자동으로 판별하지는 않습니다.

### 미분방정식

현재 미분방정식 기능은 일반해 계산을 중심으로 구현되어 있습니다.

초기조건을 별도로 입력해 자동 적용하는 기능은 아직 포함되어 있지 않습니다.

### 계산 결과

복잡한 적분, 변환 또는 미분방정식은 다음과 같은 결과가 나올 수 있습니다.

* 조건이 포함된 결과
* 계산되지 않은 적분 표현
* 특수함수가 포함된 결과
* 계산 시간이 오래 걸리는 결과

계산 결과는 반드시 문제의 정의역, 수렴 조건 및 초기조건과 함께 검토해야 합니다.

## 문제 해결

### `ModuleNotFoundError` 오류

예시:

```text
ModuleNotFoundError: No module named 'sympy'
```

필요한 라이브러리를 설치합니다.

```bash
python -m pip install -r requirements.txt
```

### `No module named tkinter` 오류

Ubuntu 또는 Debian 계열 Linux에서 다음 명령어를 실행합니다.

```bash
sudo apt install python3-tk
```

### `python` 명령어를 찾을 수 없는 경우

Windows에서는 다음 명령어를 시도합니다.

```bash
py engineering_cas_gui.py
```

또는 Python을 다시 설치하면서 다음 항목을 선택합니다.

```text
Add Python to PATH
```

### 그래프 창 또는 GUI가 나타나지 않는 경우

tkinter 테스트를 실행합니다.

```bash
python -m tkinter
```

그리고 Matplotlib를 다시 설치합니다.

```bash
python -m pip install --upgrade matplotlib
```

## 사용 라이브러리

* tkinter: GUI 구성
* SymPy: 기호 수학 및 공학수학 계산
* NumPy: 그래프용 수치 배열 계산
* Matplotlib: 함수 그래프 출력

## 향후 추가 예정 기능

* 초기조건이 포함된 미분방정식
* 양측 Z 변환 및 수렴영역 설정
* 컨볼루션 계산
* CTFS 및 DTFS
* DTFT 및 FFT
* 전달함수 계산
* Bode Plot
* Pole-Zero Map
* Root Locus
* 상태공간 모델
* 벡터 미적분
* 복소수 계산기
* 디지털 논리 계산기

## 프로젝트 목적

전자공학 및 공학수학 과목에서 자주 사용하는 계산을 하나의 GUI 프로그램으로 통합하는 것을 목표로 제작했습니다.

이 프로그램은 학습 보조 및 계산 결과 확인을 목적으로 합니다. 계산 결과를 그대로 제출하기보다는 풀이 과정과 수학적 조건을 함께 확인하는 것을 권장합니다.

## License

학습 및 개인 프로젝트 목적으로 사용할 수 있습니다.
