import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import traceback

import sympy as sp
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class EngineeringCAS:
    def __init__(self, root):
        self.root = root
        self.root.title("Engineering CAS Calculator")
        self.root.geometry("1400x850")
        self.root.minsize(1100, 700)

        # 기본 기호
        self.x, self.t, self.s, self.z, self.w = sp.symbols(
            "x t s z w", real=True
        )
        self.n, self.k = sp.symbols("n k", integer=True)
        self.y = sp.Function("y")

        self.current_result = None
        self.history = []

        self.allowed_names = {
            "x": self.x,
            "t": self.t,
            "s": self.s,
            "z": self.z,
            "w": self.w,
            "omega": self.w,
            "n": self.n,
            "k": self.k,
            "pi": sp.pi,
            "e": sp.E,
            "E": sp.E,
            "I": sp.I,
            "j": sp.I,
            "oo": sp.oo,
            "inf": sp.oo,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,
            "sinh": sp.sinh,
            "cosh": sp.cosh,
            "tanh": sp.tanh,
            "exp": sp.exp,
            "sqrt": sp.sqrt,
            "log": sp.log,
            "ln": sp.log,
            "abs": sp.Abs,
            "Abs": sp.Abs,
            "Heaviside": sp.Heaviside,
            "u": sp.Heaviside,
            "DiracDelta": sp.DiracDelta,
            "delta": sp.DiracDelta,
            "gamma": sp.gamma,
            "factorial": sp.factorial,
        }

        self.setup_style()
        self.create_widgets()
        self.set_mode("미분")
        self.draw_empty_graph()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("맑은 고딕", 19, "bold"))
        style.configure("Header.TLabel", font=("맑은 고딕", 11, "bold"))
        style.configure("TLabel", font=("맑은 고딕", 10))
        style.configure("TButton", font=("맑은 고딕", 10), padding=7)
        style.configure("TEntry", font=("Consolas", 11))
        style.configure("Treeview", font=("Consolas", 10), rowheight=27)

    def create_widgets(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(main, width=430)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)

        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(left, text="Engineering CAS", style="Title.TLabel").pack(
            anchor=tk.W, pady=(0, 4)
        )
        ttk.Label(
            left,
            text="미적분 · 라플라스 · Z 변환 · 푸리에 · 방정식 · 그래프",
        ).pack(anchor=tk.W, pady=(0, 14))

        # 연산 선택
        mode_box = ttk.LabelFrame(left, text=" 연산 선택 ", padding=10)
        mode_box.pack(fill=tk.X, pady=(0, 10))

        self.mode_var = tk.StringVar()
        self.mode_combo = ttk.Combobox(
            mode_box,
            textvariable=self.mode_var,
            state="readonly",
            values=[
                "미분",
                "부정적분",
                "정적분",
                "극한",
                "테일러 급수",
                "라플라스 변환",
                "역라플라스 변환",
                "Z 변환",
                "역 Z 변환",
                "푸리에 변환",
                "역푸리에 변환",
                "대수식 단순화",
                "인수분해",
                "전개",
                "부분분수",
                "방정식 풀기",
                "연립방정식",
                "1계 미분방정식",
                "행렬 계산",
                "함수 그래프",
            ],
        )
        self.mode_combo.pack(fill=tk.X)
        self.mode_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.set_mode(self.mode_var.get()),
        )

        # 입력
        input_box = ttk.LabelFrame(left, text=" 입력 ", padding=10)
        input_box.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_box, text="수식", style="Header.TLabel").pack(anchor=tk.W)
        self.expression_text = tk.Text(
            input_box,
            height=4,
            font=("Consolas", 11),
            wrap=tk.WORD,
        )
        self.expression_text.pack(fill=tk.X, pady=(4, 8))

        self.parameters_frame = ttk.Frame(input_box)
        self.parameters_frame.pack(fill=tk.X)

        self.param_labels = []
        self.param_entries = []

        for row in range(4):
            label = ttk.Label(self.parameters_frame, text="")
            entry = ttk.Entry(self.parameters_frame)

            label.grid(row=row, column=0, sticky=tk.W, pady=3)
            entry.grid(row=row, column=1, sticky=tk.EW, padx=(8, 0), pady=3)

            self.param_labels.append(label)
            self.param_entries.append(entry)

        self.parameters_frame.columnconfigure(1, weight=1)

        # 도움말
        help_box = ttk.LabelFrame(left, text=" 입력 예시 ", padding=10)
        help_box.pack(fill=tk.X, pady=(0, 10))

        self.help_label = ttk.Label(
            help_box,
            text="",
            justify=tk.LEFT,
            wraplength=390,
        )
        self.help_label.pack(anchor=tk.W)

        # 버튼
        button_box = ttk.Frame(left)
        button_box.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            button_box,
            text="계산",
            command=self.calculate,
        ).grid(row=0, column=0, sticky=tk.EW, padx=(0, 4), pady=3)

        ttk.Button(
            button_box,
            text="입력 지우기",
            command=self.clear_input,
        ).grid(row=0, column=1, sticky=tk.EW, padx=4, pady=3)

        ttk.Button(
            button_box,
            text="전체 초기화",
            command=self.clear_all,
        ).grid(row=1, column=0, sticky=tk.EW, padx=(0, 4), pady=3)

        ttk.Button(
            button_box,
            text="결과 저장",
            command=self.save_result,
        ).grid(row=1, column=1, sticky=tk.EW, padx=4, pady=3)

        button_box.columnconfigure(0, weight=1)
        button_box.columnconfigure(1, weight=1)

        self.status_label = ttk.Label(
            left,
            text="연산을 선택하고 수식을 입력하세요.",
            wraplength=410,
        )
        self.status_label.pack(fill=tk.X)

        # 오른쪽 노트북
        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        result_tab = ttk.Frame(self.notebook, padding=8)
        graph_tab = ttk.Frame(self.notebook, padding=8)
        history_tab = ttk.Frame(self.notebook, padding=8)

        self.notebook.add(result_tab, text="계산 결과")
        self.notebook.add(graph_tab, text="그래프")
        self.notebook.add(history_tab, text="계산 기록")

        # 결과 탭
        ttk.Label(
            result_tab,
            text="일반 표현",
            style="Header.TLabel",
        ).pack(anchor=tk.W)

        self.result_text = tk.Text(
            result_tab,
            height=12,
            font=("Consolas", 12),
            wrap=tk.WORD,
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(4, 8))

        ttk.Label(
            result_tab,
            text="LaTeX 표현",
            style="Header.TLabel",
        ).pack(anchor=tk.W)

        self.latex_text = tk.Text(
            result_tab,
            height=8,
            font=("Consolas", 11),
            wrap=tk.WORD,
        )
        self.latex_text.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        # 그래프 탭
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, graph_tab)
        toolbar.update()

        # 기록 탭
        columns = ("mode", "input", "result")
        self.history_tree = ttk.Treeview(
            history_tab,
            columns=columns,
            show="headings",
        )
        self.history_tree.heading("mode", text="연산")
        self.history_tree.heading("input", text="입력")
        self.history_tree.heading("result", text="결과")

        self.history_tree.column("mode", width=150, anchor=tk.CENTER)
        self.history_tree.column("input", width=350)
        self.history_tree.column("result", width=500)

        scrollbar = ttk.Scrollbar(
            history_tab,
            orient=tk.VERTICAL,
            command=self.history_tree.yview,
        )
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_tree.bind(
            "<Double-1>",
            self.load_history_item,
        )

        # 단축키
        self.root.bind("<Control-Return>", lambda event: self.calculate())
        self.root.bind("<F5>", lambda event: self.calculate())

    def set_mode(self, mode):
        self.mode_var.set(mode)

        settings = {
            "미분": (
                "sin(x)*exp(x)",
                [("변수", "x"), ("미분 차수", "1")],
                "예: sin(x)*exp(x)\nCtrl+Enter 또는 F5로 계산",
            ),
            "부정적분": (
                "x*exp(x)",
                [("적분 변수", "x")],
                "예: x*exp(x)",
            ),
            "정적분": (
                "sin(x)",
                [("적분 변수", "x"), ("하한", "0"), ("상한", "pi")],
                "예: sin(x), 하한 0, 상한 pi",
            ),
            "극한": (
                "sin(x)/x",
                [("변수", "x"), ("접근값", "0"), ("방향", "+-")],
                "방향: +, -, +- 중 하나",
            ),
            "테일러 급수": (
                "exp(x)",
                [("변수", "x"), ("중심", "0"), ("차수", "6")],
                "예: exp(x), 중심 0, 차수 6",
            ),
            "라플라스 변환": (
                "exp(-2*t)*sin(3*t)",
                [("시간 변수", "t"), ("복소 변수", "s")],
                "예: exp(-2*t)*sin(3*t)",
            ),
            "역라플라스 변환": (
                "1/(s**2 + 4)",
                [("복소 변수", "s"), ("시간 변수", "t")],
                "예: 1/(s**2+4)",
            ),
            "Z 변환": (
                "(1/2)**n",
                [("이산 변수", "n"), ("Z 변수", "z"), ("시작 n", "0")],
                "단측 Z 변환: Σ x[n] z^(-n), n=시작값부터 ∞",
            ),
            "역 Z 변환": (
                "z/(z - 1/2)",
                [("Z 변수", "z"), ("이산 변수", "n"), ("계열 차수", "12")],
                "z=∞ 부근의 z^(-1) 급수로 계수를 구합니다.",
            ),
            "푸리에 변환": (
                "exp(-t**2)",
                [("시간 변수", "t"), ("주파수 변수", "w")],
                "정의: ∫f(t)e^(-j*w*t)dt",
            ),
            "역푸리에 변환": (
                "sqrt(pi)*exp(-w**2/4)",
                [("주파수 변수", "w"), ("시간 변수", "t")],
                "SymPy 기본 역푸리에 정의를 사용합니다.",
            ),
            "대수식 단순화": (
                "(x**2 - 1)/(x - 1)",
                [],
                "예: (x**2-1)/(x-1)",
            ),
            "인수분해": (
                "x**3 - x",
                [],
                "예: x**3-x",
            ),
            "전개": (
                "(x + 1)**4",
                [],
                "예: (x+1)**4",
            ),
            "부분분수": (
                "(2*s + 3)/(s*(s + 1))",
                [("변수", "s")],
                "예: (2*s+3)/(s*(s+1))",
            ),
            "방정식 풀기": (
                "x**2 - 5*x + 6 = 0",
                [("변수", "x")],
                "등호를 포함하거나 식=0 형태로 입력",
            ),
            "연립방정식": (
                "x + 2*y = 5; 3*x - y = 4",
                [("변수들", "x,y")],
                "세미콜론(;)으로 식을 구분",
            ),
            "1계 미분방정식": (
                "Derivative(y(x), x) + y(x) = exp(x)",
                [("독립 변수", "x")],
                "예: Derivative(y(x),x)+y(x)=exp(x)",
            ),
            "행렬 계산": (
                "[[1,2],[3,4]]",
                [("연산", "det"), ("두 번째 행렬", "")],
                "연산: det, inv, transpose, eigen, rank, add, multiply",
            ),
            "함수 그래프": (
                "sin(x)",
                [("변수", "x"), ("최솟값", "-10"), ("최댓값", "10"), ("점 개수", "1000")],
                "여러 함수는 세미콜론으로 구분: sin(x); cos(x)",
            ),
        }

        expression, params, help_text = settings[mode]

        self.expression_text.delete("1.0", tk.END)
        self.expression_text.insert("1.0", expression)

        for label, entry in zip(self.param_labels, self.param_entries):
            label.configure(text="")
            entry.delete(0, tk.END)
            label.grid_remove()
            entry.grid_remove()

        for index, (label_text, value) in enumerate(params):
            self.param_labels[index].configure(text=label_text)
            self.param_entries[index].insert(0, value)
            self.param_labels[index].grid()
            self.param_entries[index].grid()

        self.help_label.configure(text=help_text)
        self.status_label.configure(text=f"{mode} 모드")

    def parse_expr(self, text):
        text = text.strip().replace("^", "**")
        if not text:
            raise ValueError("수식을 입력하세요.")

        local_dict = dict(self.allowed_names)
        local_dict["y"] = self.y
        local_dict["Derivative"] = sp.Derivative
        local_dict["Integral"] = sp.Integral
        local_dict["Matrix"] = sp.Matrix

        return sp.sympify(text, locals=local_dict)

    def get_symbol(self, name):
        name = name.strip()
        if not name:
            raise ValueError("변수를 입력하세요.")

        if name in self.allowed_names and isinstance(
            self.allowed_names[name], sp.Symbol
        ):
            return self.allowed_names[name]

        symbol = sp.Symbol(name)
        self.allowed_names[name] = symbol
        return symbol

    def get_param(self, index, default=""):
        value = self.param_entries[index].get().strip()
        return value if value else default

    def split_equation(self, text):
        if "=" in text:
            left, right = text.split("=", 1)
            return sp.Eq(self.parse_expr(left), self.parse_expr(right))
        return sp.Eq(self.parse_expr(text), 0)

    def calculate(self):
        mode = self.mode_var.get()
        input_text = self.expression_text.get("1.0", tk.END).strip()

        try:
            result = self.perform_operation(mode, input_text)
            self.current_result = result

            self.show_result(result)
            self.add_history(mode, input_text, result)

            self.status_label.configure(text=f"{mode} 계산 완료")
            self.notebook.select(0)

        except Exception as error:
            self.status_label.configure(text=f"오류: {error}")
            messagebox.showerror(
                "계산 오류",
                f"{error}\n\n입력식과 변수를 확인하세요.",
            )

    def perform_operation(self, mode, input_text):
        if mode == "미분":
            expr = self.parse_expr(input_text)
            var = self.get_symbol(self.get_param(0, "x"))
            order = int(self.get_param(1, "1"))
            return sp.diff(expr, var, order)

        if mode == "부정적분":
            expr = self.parse_expr(input_text)
            var = self.get_symbol(self.get_param(0, "x"))
            return sp.integrate(expr, var)

        if mode == "정적분":
            expr = self.parse_expr(input_text)
            var = self.get_symbol(self.get_param(0, "x"))
            lower = self.parse_expr(self.get_param(1, "0"))
            upper = self.parse_expr(self.get_param(2, "1"))
            return sp.integrate(expr, (var, lower, upper))

        if mode == "극한":
            expr = self.parse_expr(input_text)
            var = self.get_symbol(self.get_param(0, "x"))
            point = self.parse_expr(self.get_param(1, "0"))
            direction = self.get_param(2, "+-")
            return sp.limit(expr, var, point, dir=direction)

        if mode == "테일러 급수":
            expr = self.parse_expr(input_text)
            var = self.get_symbol(self.get_param(0, "x"))
            center = self.parse_expr(self.get_param(1, "0"))
            order = int(self.get_param(2, "6"))
            return sp.series(expr, var, center, order)

        if mode == "라플라스 변환":
            expr = self.parse_expr(input_text)
            time_var = self.get_symbol(self.get_param(0, "t"))
            complex_var = self.get_symbol(self.get_param(1, "s"))
            return sp.laplace_transform(
                expr,
                time_var,
                complex_var,
                noconds=False,
            )

        if mode == "역라플라스 변환":
            expr = self.parse_expr(input_text)
            complex_var = self.get_symbol(self.get_param(0, "s"))
            time_var = self.get_symbol(self.get_param(1, "t"))
            return sp.inverse_laplace_transform(
                expr,
                complex_var,
                time_var,
            )

        if mode == "Z 변환":
            expr = self.parse_expr(input_text)
            discrete_var = self.get_symbol(self.get_param(0, "n"))
            z_var = self.get_symbol(self.get_param(1, "z"))
            start = int(self.get_param(2, "0"))

            transform = sp.summation(
                expr * z_var ** (-discrete_var),
                (discrete_var, start, sp.oo),
            )
            return sp.simplify(transform)

        if mode == "역 Z 변환":
            expr = self.parse_expr(input_text)
            z_var = self.get_symbol(self.get_param(0, "z"))
            discrete_var = self.get_symbol(self.get_param(1, "n"))
            order = int(self.get_param(2, "12"))

            q = sp.Symbol("q")
            q_expr = sp.simplify(expr.subs(z_var, 1 / q))
            expansion = sp.series(q_expr, q, 0, order).removeO().expand()

            sequence = []
            for index in range(order):
                coefficient = sp.simplify(expansion.coeff(q, index))
                sequence.append((index, coefficient))

            return sequence

        if mode == "푸리에 변환":
            expr = self.parse_expr(input_text)
            time_var = self.get_symbol(self.get_param(0, "t"))
            freq_var = self.get_symbol(self.get_param(1, "w"))

            integral = sp.integrate(
                expr * sp.exp(-sp.I * freq_var * time_var),
                (time_var, -sp.oo, sp.oo),
            )
            return sp.simplify(integral)

        if mode == "역푸리에 변환":
            expr = self.parse_expr(input_text)
            freq_var = self.get_symbol(self.get_param(0, "w"))
            time_var = self.get_symbol(self.get_param(1, "t"))

            integral = sp.integrate(
                expr * sp.exp(sp.I * freq_var * time_var),
                (freq_var, -sp.oo, sp.oo),
            ) / (2 * sp.pi)
            return sp.simplify(integral)

        if mode == "대수식 단순화":
            return sp.simplify(self.parse_expr(input_text))

        if mode == "인수분해":
            return sp.factor(self.parse_expr(input_text))

        if mode == "전개":
            return sp.expand(self.parse_expr(input_text))

        if mode == "부분분수":
            expr = self.parse_expr(input_text)
            var = self.get_symbol(self.get_param(0, "x"))
            return sp.apart(expr, var)

        if mode == "방정식 풀기":
            equation = self.split_equation(input_text)
            var = self.get_symbol(self.get_param(0, "x"))
            return sp.solve(equation, var)

        if mode == "연립방정식":
            equation_texts = [
                item.strip()
                for item in input_text.split(";")
                if item.strip()
            ]
            equations = [self.split_equation(item) for item in equation_texts]

            variable_names = [
                item.strip()
                for item in self.get_param(0, "x,y").split(",")
                if item.strip()
            ]
            variables = [self.get_symbol(name) for name in variable_names]
            return sp.solve(equations, variables, dict=True)

        if mode == "1계 미분방정식":
            equation = self.split_equation(input_text)
            independent_var = self.get_symbol(self.get_param(0, "x"))
            dependent = self.y(independent_var)
            return sp.dsolve(equation, dependent)

        if mode == "행렬 계산":
            matrix_a = sp.Matrix(self.parse_expr(input_text))
            operation = self.get_param(0, "det").lower()
            second_text = self.get_param(1, "")

            if operation == "det":
                return matrix_a.det()
            if operation == "inv":
                return matrix_a.inv()
            if operation == "transpose":
                return matrix_a.T
            if operation == "eigen":
                return matrix_a.eigenvals()
            if operation == "rank":
                return matrix_a.rank()

            if not second_text:
                raise ValueError("두 번째 행렬을 입력하세요.")

            matrix_b = sp.Matrix(self.parse_expr(second_text))

            if operation == "add":
                return matrix_a + matrix_b
            if operation == "multiply":
                return matrix_a * matrix_b

            raise ValueError(
                "지원 연산: det, inv, transpose, eigen, rank, add, multiply"
            )

        if mode == "함수 그래프":
            self.plot_functions(input_text)
            return "그래프를 생성했습니다."

        raise ValueError("지원하지 않는 연산입니다.")

    def show_result(self, result):
        self.result_text.delete("1.0", tk.END)
        self.latex_text.delete("1.0", tk.END)

        if isinstance(result, list) and result and isinstance(result[0], tuple):
            plain = "\n".join(
                f"x[{index}] = {value}"
                for index, value in result
            )
            latex = r"\begin{aligned}" + " \\\\ ".join(
                f"x[{index}] &= {sp.latex(value)}"
                for index, value in result
            ) + r"\end{aligned}"
        else:
            plain = sp.pretty(result, use_unicode=True)
            latex = sp.latex(result)

        self.result_text.insert("1.0", plain)
        self.latex_text.insert("1.0", latex)

    def plot_functions(self, input_text):
        variable = self.get_symbol(self.get_param(0, "x"))
        x_min = float(self.get_param(1, "-10"))
        x_max = float(self.get_param(2, "10"))
        points = int(self.get_param(3, "1000"))

        if x_min >= x_max:
            raise ValueError("최솟값은 최댓값보다 작아야 합니다.")
        if points < 10 or points > 200000:
            raise ValueError("점 개수는 10~200000 사이여야 합니다.")

        expressions = [
            item.strip()
            for item in input_text.split(";")
            if item.strip()
        ]
        if not expressions:
            raise ValueError("그래프 수식을 입력하세요.")

        x_values = np.linspace(x_min, x_max, points)

        self.ax.clear()

        for expression_text in expressions:
            expression = self.parse_expr(expression_text)
            function = sp.lambdify(variable, expression, modules=["numpy"])

            with np.errstate(
                divide="ignore",
                invalid="ignore",
                over="ignore",
            ):
                y_values = function(x_values)

            if np.isscalar(y_values):
                y_values = np.full_like(x_values, float(y_values))

            y_values = np.asarray(y_values, dtype=np.complex128)

            if np.any(np.abs(y_values.imag) > 1e-9):
                raise ValueError(
                    f"{expression_text}: 복소수 출력이 발생했습니다."
                )

            y_values = y_values.real
            y_values[~np.isfinite(y_values)] = np.nan

            self.ax.plot(
                x_values,
                y_values,
                linewidth=2,
                label=expression_text,
            )

        self.ax.axhline(0, linewidth=0.8)
        self.ax.axvline(0, linewidth=0.8)
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.ax.set_xlabel(str(variable))
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Function Graph")
        self.ax.legend()

        self.figure.tight_layout()
        self.canvas.draw()
        self.notebook.select(1)

    def draw_empty_graph(self):
        self.ax.clear()
        self.ax.set_title("Function Graph")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.ax.axhline(0, linewidth=0.8)
        self.ax.axvline(0, linewidth=0.8)
        self.figure.tight_layout()
        self.canvas.draw()

    def add_history(self, mode, input_text, result):
        try:
            result_text = str(result)
        except Exception:
            result_text = "<표시할 수 없음>"

        if len(input_text) > 100:
            input_display = input_text[:97] + "..."
        else:
            input_display = input_text

        if len(result_text) > 160:
            result_display = result_text[:157] + "..."
        else:
            result_display = result_text

        self.history.append((mode, input_text, result_text))
        self.history_tree.insert(
            "",
            tk.END,
            values=(mode, input_display, result_display),
        )

    def load_history_item(self, event):
        selection = self.history_tree.selection()
        if not selection:
            return

        index = self.history_tree.index(selection[0])
        mode, input_text, _ = self.history[index]

        self.set_mode(mode)
        self.expression_text.delete("1.0", tk.END)
        self.expression_text.insert("1.0", input_text)

    def clear_input(self):
        self.expression_text.delete("1.0", tk.END)
        for entry in self.param_entries:
            if entry.winfo_ismapped():
                entry.delete(0, tk.END)
        self.status_label.configure(text="입력을 지웠습니다.")

    def clear_all(self):
        self.result_text.delete("1.0", tk.END)
        self.latex_text.delete("1.0", tk.END)
        self.history_tree.delete(*self.history_tree.get_children())
        self.history.clear()
        self.current_result = None
        self.draw_empty_graph()
        self.set_mode("미분")
        self.status_label.configure(text="전체 초기화 완료")

    def save_result(self):
        if self.current_result is None:
            messagebox.showwarning("저장", "저장할 계산 결과가 없습니다.")
            return

        file_path = filedialog.asksaveasfilename(
            title="계산 결과 저장",
            defaultextension=".txt",
            filetypes=[
                ("텍스트 파일", "*.txt"),
                ("LaTeX 파일", "*.tex"),
                ("모든 파일", "*.*"),
            ],
        )

        if not file_path:
            return

        try:
            if file_path.lower().endswith(".tex"):
                content = sp.latex(self.current_result)
            else:
                content = (
                    "일반 표현\n"
                    "=========\n"
                    f"{sp.pretty(self.current_result, use_unicode=True)}\n\n"
                    "LaTeX 표현\n"
                    "==========\n"
                    f"{sp.latex(self.current_result)}\n"
                )

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

            messagebox.showinfo("저장 완료", file_path)

        except Exception as error:
            messagebox.showerror("저장 오류", str(error))


def main():
    root = tk.Tk()
    app = EngineeringCAS(root)
    root.mainloop()


if __name__ == "__main__":
    main()
