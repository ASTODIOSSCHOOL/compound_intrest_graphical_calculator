import math
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class CompoundInterestApp(ctk.CTk):
	def __init__(self):
		super().__init__()

		self.title("Compound Interest Calculator")
		self.geometry("1100x700")
		self.minsize(900, 600)

		ctk.set_appearance_mode("System")
		ctk.set_default_color_theme("blue")

		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self._build_controls()
		self._build_chart()
		self.calculate()

	def _build_controls(self):
		self.controls = ctk.CTkFrame(self, corner_radius=0)
		self.controls.grid(row=0, column=0, sticky="nsew")
		self.controls.grid_columnconfigure(0, weight=1)

		ctk.CTkLabel(
			self.controls,
			text="Compound Interest",
			font=ctk.CTkFont(size=24, weight="bold"),
		).grid(row=0, column=0, padx=24, pady=(30, 6), sticky="w")
		ctk.CTkLabel(
			self.controls,
			text="See how your money grows over time.",
			text_color="gray",
		).grid(row=1, column=0, padx=24, pady=(0, 28), sticky="w")

		self.principal_entry = self._add_input("Initial amount", "₹", 2, "1000")
		self.rate_entry = self._add_input("Annual interest rate", "%", 4, "5")
		self.years_entry = self._add_input("Time period", "years", 6, "10")

		ctk.CTkLabel(self.controls, text="Compounds per year").grid(
			row=8, column=0, padx=24, pady=(16, 5), sticky="w"
		)
		self.frequency_menu = ctk.CTkOptionMenu(
			self.controls,
			values=["Annually", "Semi-annually", "Quarterly", "Monthly", "Daily"],
		)
		self.frequency_menu.set("Annually")
		self.frequency_menu.grid(row=9, column=0, padx=24, sticky="ew")

		ctk.CTkButton(
			self.controls,
			text="Calculate",
			height=40,
			command=self.calculate,
		).grid(row=10, column=0, padx=24, pady=(28, 20), sticky="ew")

		self.result_label = ctk.CTkLabel(
			self.controls,
			text="",
			justify="left",
			anchor="w",
			font=ctk.CTkFont(size=15),
		)
		self.result_label.grid(row=11, column=0, padx=24, pady=4, sticky="ew")

	def _add_input(self, label, suffix, row, default):
		ctk.CTkLabel(self.controls, text=label).grid(
			row=row, column=0, padx=24, pady=(10, 5), sticky="w"
		)
		frame = ctk.CTkFrame(self.controls, fg_color="transparent")
		frame.grid(row=row + 1, column=0, padx=24, sticky="ew")
		frame.grid_columnconfigure(0, weight=1)

		entry = ctk.CTkEntry(frame)
		entry.insert(0, default)
		entry.grid(row=0, column=0, sticky="ew")
		ctk.CTkLabel(frame, text=suffix, text_color="gray").grid(
			row=0, column=1, padx=(8, 0)
		)
		return entry

	def _build_chart(self):
		chart_frame = ctk.CTkFrame(self, fg_color="transparent")
		chart_frame.grid(row=0, column=1, padx=(10, 24), pady=24, sticky="nsew")
		chart_frame.grid_rowconfigure(0, weight=1)
		chart_frame.grid_columnconfigure(0, weight=1)

		self.figure = Figure(figsize=(7, 5), dpi=100)
		self.axis = self.figure.add_subplot(111)
		self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
		self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

	def _frequency(self):
		return {
			"Annually": 1,
			"Semi-annually": 2,
			"Quarterly": 4,
			"Monthly": 12,
			"Daily": 365,
		}[self.frequency_menu.get()]

	def _values(self):
		principal_text = self.principal_entry.get().strip().replace(",", "")
		rate_text = self.rate_entry.get().strip().replace(",", "")
		years_text = self.years_entry.get().strip().replace(",", "")
		if not principal_text or not rate_text or not years_text:
			raise ValueError("Fill in all fields.")

		principal = float(principal_text)
		rate = float(rate_text) / 100
		years = float(years_text)
		frequency = self._frequency()

		if not all(math.isfinite(value) for value in (principal, rate, years)):
			raise ValueError("Enter finite numbers in all fields.")
		if principal < 0 or rate < 0 or years <= 0:
			raise ValueError("Amount and rate must be non-negative; time must be positive.")

		points = max(2, math.ceil(years * 12) + 1)
		times = [years * index / (points - 1) for index in range(points)]
		balances = [
			principal * (1 + rate / frequency) ** (frequency * time)
			for time in times
		]
		return principal, rate, years, times, balances

	def calculate(self):
		try:
			principal, rate, years, times, balances = self._values()
		except (ValueError, KeyError) as error:
			messagebox.showerror(
				"Invalid input",
				str(error),
			)
			return

		final_balance = balances[-1]
		interest = final_balance - principal
		self.result_label.configure(
			text=(
				f"Final balance\n₹{final_balance:,.2f}\n\n"
				f"Interest earned\n₹{interest:,.2f}\n\n"
				f"Growth\n{(final_balance / principal - 1) * 100:.2f}%"
				if principal
				else "Final balance\n₹0.00\n\nInterest earned\n₹0.00\n\nGrowth\n0.00%"
			)
		)

		self.axis.clear()
		self.axis.plot(times, balances, color="#2563eb", linewidth=2.5)
		self.axis.fill_between(times, balances, color="#2563eb", alpha=0.12)
		self.axis.set_title("Balance over time")
		self.axis.set_xlabel("Years")
		self.axis.set_ylabel("Balance (₹)")
		self.axis.grid(alpha=0.25)
		self.figure.tight_layout()
		self.canvas.draw()


if __name__ == "__main__":
	app = CompoundInterestApp()
	app.mainloop()
