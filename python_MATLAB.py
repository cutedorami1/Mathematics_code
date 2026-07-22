import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import numpy as np
import sympy as sp

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class PythonMatlabGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python MATLAB 그래프 프로그램")
        self.root.geometry("1200x750")
        self.root.minsize(950, 650)

        # SymPy에서 사용할 변수
        self.x_symbol = sp.Symbol("x")

        # 그래프 번호
        self.plot_count = 0

        # 스타일 설정
        self.setup_style()

        # GUI 구성
        self.create_widgets()

        # 기본 그래프 설정
        self.initialize_graph()

    def setup_style(self):
        """GUI 스타일 설정"""
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("맑은 고딕", 18, "bold")
        )

        style.configure(
            "Section.TLabel",
            font=("맑은 고딕", 11, "bold")
        )

        style.configure(
            "TButton",
            font=("맑은 고딕", 10),
            padding=7
        )

        style.configure(
            "TLabel",
            font=("맑은 고딕", 10)
        )

        style.configure(
            "TEntry",
            font=("Consolas", 11)
        )

    def create_widgets(self):
        """전체 GUI 구성"""

        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 왼쪽 제어 영역
        control_frame = ttk.LabelFrame(
            main_frame,
            text=" 그래프 설정 ",
            padding=15
        )
        control_frame.pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=(0, 12)
        )

        # 오른쪽 그래프 영역
        graph_frame = ttk.Frame(main_frame)
        graph_frame.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=True
        )

        # 제목
        title_label = ttk.Label(
            control_frame,
            text="Python MATLAB",
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = ttk.Label(
            control_frame,
            text="함수를 입력하여 그래프를 그립니다."
        )
        subtitle_label.pack(pady=(0, 20))

        # 함수 입력
        ttk.Label(
            control_frame,
            text="함수 y =",
            style="Section.TLabel"
        ).pack(anchor=tk.W)

        self.function_entry = ttk.Entry(
            control_frame,
            width=32
        )
        self.function_entry.pack(
            fill=tk.X,
            pady=(5, 5)
        )
        self.function_entry.insert(0, "sin(x)")

        function_help = ttk.Label(
            control_frame,
            text=(
                "예시\n"
                "sin(x)\n"
                "cos(x)\n"
                "x**2\n"
                "exp(-x)\n"
                "sin(x) + cos(2*x)"
            ),
            justify=tk.LEFT
        )
        function_help.pack(
            anchor=tk.W,
            pady=(0, 18)
        )

        # x축 범위
        ttk.Label(
            control_frame,
            text="x축 범위",
            style="Section.TLabel"
        ).pack(anchor=tk.W)

        range_frame = ttk.Frame(control_frame)
        range_frame.pack(
            fill=tk.X,
            pady=(7, 15)
        )

        ttk.Label(range_frame, text="최솟값").grid(
            row=0,
            column=0,
            sticky=tk.W
        )

        self.x_min_entry = ttk.Entry(
            range_frame,
            width=10
        )
        self.x_min_entry.grid(
            row=1,
            column=0,
            padx=(0, 8)
        )
        self.x_min_entry.insert(0, "-10")

        ttk.Label(range_frame, text="최댓값").grid(
            row=0,
            column=1,
            sticky=tk.W
        )

        self.x_max_entry = ttk.Entry(
            range_frame,
            width=10
        )
        self.x_max_entry.grid(
            row=1,
            column=1
        )
        self.x_max_entry.insert(0, "10")

        # 점 개수
        ttk.Label(
            control_frame,
            text="그래프 점 개수",
            style="Section.TLabel"
        ).pack(anchor=tk.W)

        self.point_count_entry = ttk.Entry(
            control_frame
        )
        self.point_count_entry.pack(
            fill=tk.X,
            pady=(5, 15)
        )
        self.point_count_entry.insert(0, "1000")

        # 그래프 제목
        ttk.Label(
            control_frame,
            text="그래프 제목",
            style="Section.TLabel"
        ).pack(anchor=tk.W)

        self.title_entry = ttk.Entry(
            control_frame
        )
        self.title_entry.pack(
            fill=tk.X,
            pady=(5, 15)
        )
        self.title_entry.insert(0, "Function Graph")

        # 선 모양 선택
        ttk.Label(
            control_frame,
            text="선 모양",
            style="Section.TLabel"
        ).pack(anchor=tk.W)

        self.line_style_combo = ttk.Combobox(
            control_frame,
            state="readonly",
            values=[
                "실선",
                "점선",
                "파선",
                "점-파선"
            ]
        )
        self.line_style_combo.pack(
            fill=tk.X,
            pady=(5, 15)
        )
        self.line_style_combo.current(0)

        # 옵션
        ttk.Label(
            control_frame,
            text="표시 옵션",
            style="Section.TLabel"
        ).pack(anchor=tk.W)

        self.grid_var = tk.BooleanVar(value=True)
        self.legend_var = tk.BooleanVar(value=True)
        self.axis_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            control_frame,
            text="격자 표시",
            variable=self.grid_var,
            command=self.update_options
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            control_frame,
            text="범례 표시",
            variable=self.legend_var,
            command=self.update_options
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            control_frame,
            text="x축과 y축 표시",
            variable=self.axis_var,
            command=self.update_options
        ).pack(anchor=tk.W, pady=2)

        # 버튼 영역
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(
            fill=tk.X,
            pady=(20, 0)
        )

        plot_button = ttk.Button(
            button_frame,
            text="그래프 그리기",
            command=self.plot_function
        )
        plot_button.pack(fill=tk.X, pady=4)

        add_button = ttk.Button(
            button_frame,
            text="그래프 추가",
            command=self.add_function
        )
        add_button.pack(fill=tk.X, pady=4)

        clear_button = ttk.Button(
            button_frame,
            text="그래프 지우기",
            command=self.clear_graph
        )
        clear_button.pack(fill=tk.X, pady=4)

        save_button = ttk.Button(
            button_frame,
            text="그래프 이미지 저장",
            command=self.save_graph
        )
        save_button.pack(fill=tk.X, pady=4)

        # 상태 표시
        ttk.Separator(
            control_frame,
            orient=tk.HORIZONTAL
        ).pack(fill=tk.X, pady=15)

        self.status_label = ttk.Label(
            control_frame,
            text="함수를 입력한 후 그래프 그리기를 누르세요.",
            wraplength=260
        )
        self.status_label.pack(anchor=tk.W)

        # Matplotlib Figure
        self.figure = Figure(
            figsize=(8, 6),
            dpi=100
        )

        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_frame
        )

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

        # 확대, 축소, 이동, 저장 도구
        toolbar = NavigationToolbar2Tk(
            self.canvas,
            graph_frame
        )
        toolbar.update()

        # Enter 키를 누르면 그래프 그리기
        self.function_entry.bind(
            "<Return>",
            lambda event: self.plot_function()
        )

    def initialize_graph(self):
        """초기 그래프 화면 설정"""
        self.ax.set_title("Function Graph")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        self.ax.axhline(0, linewidth=0.8)
        self.ax.axvline(0, linewidth=0.8)

        self.figure.tight_layout()
        self.canvas.draw()

    def get_line_style(self):
        """선 모양 반환"""
        style_name = self.line_style_combo.get()

        line_styles = {
            "실선": "-",
            "점선": ":",
            "파선": "--",
            "점-파선": "-."
        }

        return line_styles.get(style_name, "-")

    def convert_expression(self, expression_text):
        """
        사용자가 입력한 수식을 SymPy 수식으로 변환합니다.

        예:
        sin(x)
        x^2
        exp(-x)
        """

        # ^를 Python 거듭제곱 연산자로 변환
        expression_text = expression_text.replace("^", "**")

        # 사용할 수 있는 함수 제한
        allowed_functions = {
            "x": self.x_symbol,
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
            "pi": sp.pi,
            "e": sp.E
        }

        expression = sp.sympify(
            expression_text,
            locals=allowed_functions
        )

        # x 이외의 알 수 없는 변수가 있는지 확인
        unknown_symbols = expression.free_symbols - {self.x_symbol}

        if unknown_symbols:
            raise ValueError(
                f"사용할 수 없는 변수가 있습니다: {unknown_symbols}"
            )

        return expression

    def get_graph_data(self):
        """입력값을 읽어서 x, y 데이터를 생성"""

        expression_text = self.function_entry.get().strip()

        if not expression_text:
            raise ValueError("함수를 입력하세요.")

        try:
            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())
        except ValueError:
            raise ValueError(
                "x축 최솟값과 최댓값은 숫자로 입력해야 합니다."
            )

        if x_min >= x_max:
            raise ValueError(
                "x축 최솟값은 최댓값보다 작아야 합니다."
            )

        try:
            point_count = int(self.point_count_entry.get())
        except ValueError:
            raise ValueError(
                "그래프 점 개수는 정수로 입력해야 합니다."
            )

        if point_count < 10:
            raise ValueError(
                "그래프 점 개수는 10 이상이어야 합니다."
            )

        if point_count > 100000:
            raise ValueError(
                "그래프 점 개수는 100000 이하로 설정하세요."
            )

        expression = self.convert_expression(expression_text)

        # SymPy 수식을 NumPy 함수로 변환
        function = sp.lambdify(
            self.x_symbol,
            expression,
            modules=["numpy"]
        )

        x_values = np.linspace(
            x_min,
            x_max,
            point_count
        )

        with np.errstate(
            divide="ignore",
            invalid="ignore",
            over="ignore"
        ):
            y_values = function(x_values)

        # y가 상수일 경우 배열로 변환
        if np.isscalar(y_values):
            y_values = np.full_like(
                x_values,
                float(y_values),
                dtype=float
            )

        y_values = np.asarray(
            y_values,
            dtype=np.complex128
        )

        # 복소수 결과 처리
        if np.any(np.abs(y_values.imag) > 1e-10):
            raise ValueError(
                "현재 설정한 x 범위에서 복소수 결과가 발생했습니다."
            )

        y_values = y_values.real

        # 무한대 값을 NaN으로 변경해 그래프 선이 튀는 현상 방지
        y_values[~np.isfinite(y_values)] = np.nan

        return (
            expression_text,
            expression,
            x_values,
            y_values
        )

    def plot_function(self):
        """기존 그래프를 지우고 새로운 그래프 그리기"""

        try:
            expression_text, expression, x_values, y_values = (
                self.get_graph_data()
            )

            self.ax.clear()
            self.plot_count = 0

            self.draw_plot(
                expression_text,
                x_values,
                y_values
            )

            self.status_label.config(
                text=f"그래프 생성 완료: y = {expression}"
            )

        except Exception as error:
            messagebox.showerror(
                "그래프 오류",
                str(error)
            )

            self.status_label.config(
                text=f"오류: {error}"
            )

    def add_function(self):
        """기존 그래프를 유지하고 새로운 함수 추가"""

        try:
            expression_text, expression, x_values, y_values = (
                self.get_graph_data()
            )

            self.draw_plot(
                expression_text,
                x_values,
                y_values
            )

            self.status_label.config(
                text=f"그래프 추가 완료: y = {expression}"
            )

        except Exception as error:
            messagebox.showerror(
                "그래프 오류",
                str(error)
            )

            self.status_label.config(
                text=f"오류: {error}"
            )

    def draw_plot(
        self,
        expression_text,
        x_values,
        y_values
    ):
        """실제 그래프 출력"""

        self.plot_count += 1

        line_style = self.get_line_style()

        self.ax.plot(
            x_values,
            y_values,
            linestyle=line_style,
            linewidth=2,
            label=f"y = {expression_text}"
        )

        graph_title = self.title_entry.get().strip()

        if not graph_title:
            graph_title = "Function Graph"

        self.ax.set_title(
            graph_title,
            fontsize=14,
            fontweight="bold"
        )

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        self.apply_graph_options()

        self.figure.tight_layout()
        self.canvas.draw()

    def apply_graph_options(self):
        """격자, 범례, 좌표축 옵션 적용"""

        self.ax.grid(
            self.grid_var.get(),
            linestyle="--",
            alpha=0.5
        )

        # 기존 x축과 y축 선 제거
        for line in list(self.ax.lines):
            if getattr(line, "_is_axis_line", False):
                line.remove()

        if self.axis_var.get():
            horizontal_line = self.ax.axhline(
                0,
                linewidth=0.8
            )
            horizontal_line._is_axis_line = True

            vertical_line = self.ax.axvline(
                0,
                linewidth=0.8
            )
            vertical_line._is_axis_line = True

        legend = self.ax.get_legend()

        if self.legend_var.get() and self.plot_count > 0:
            self.ax.legend()
        elif legend is not None:
            legend.remove()

    def update_options(self):
        """체크박스 변경 시 그래프 갱신"""

        self.apply_graph_options()
        self.figure.tight_layout()
        self.canvas.draw()

    def clear_graph(self):
        """그래프 모두 지우기"""

        self.ax.clear()
        self.plot_count = 0

        self.ax.set_title("Function Graph")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        self.apply_graph_options()

        self.figure.tight_layout()
        self.canvas.draw()

        self.status_label.config(
            text="그래프를 모두 지웠습니다."
        )

    def save_graph(self):
        """그래프를 이미지 파일로 저장"""

        file_path = filedialog.asksaveasfilename(
            title="그래프 이미지 저장",
            defaultextension=".png",
            filetypes=[
                ("PNG 이미지", "*.png"),
                ("JPEG 이미지", "*.jpg"),
                ("PDF 문서", "*.pdf"),
                ("SVG 벡터 이미지", "*.svg"),
                ("모든 파일", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            self.figure.savefig(
                file_path,
                dpi=300,
                bbox_inches="tight"
            )

            messagebox.showinfo(
                "저장 완료",
                f"그래프를 저장했습니다.\n\n{file_path}"
            )

            self.status_label.config(
                text=f"이미지 저장 완료: {file_path}"
            )

        except Exception as error:
            messagebox.showerror(
                "저장 오류",
                f"파일을 저장하지 못했습니다.\n{error}"
            )


def main():
    root = tk.Tk()
    app = PythonMatlabGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
