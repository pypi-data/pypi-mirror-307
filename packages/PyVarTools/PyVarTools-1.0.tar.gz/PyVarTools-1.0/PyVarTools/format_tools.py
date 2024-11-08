from typing import Any
from pandas import DataFrame
#
#
#
#
def format_integer(number: int, class_sep: str = " "):
	return "{:,d}".format(number).replace(",", class_sep)
#
#
#
#
def format_float(number: float, class_sep: str = " ", number_of_decimals: int = 2):
	return ("{:,.%df}" % number_of_decimals).format(number).replace(",", class_sep)
#
#
#
#
def format_data_frame(
		data_frame: DataFrame,
		float_format: str | Any = "%.2f",
		integer_format: str | Any = "%d",
		columns_split: str | None = " || ",
		header_border: str | None = "=",
		top_border: str | None = "=",
		left_border: str | None = "|| ",
		bottom_border: str | None = "=",
		right_border: str | None = " ||"
):
	float_format_is_string = type(float_format) == str
	integer_format_is_string = type(integer_format) == str

	new_dataframe = {}
	for column, values in data_frame.items():
		new_dataframe[column] = []

		for i in range(len(values)):
			value = data_frame[column].iloc[i]
			if str(type(value)).startswith("<class 'numpy"):
				value = value.item()

			if type(value) == int:
				if integer_format_is_string:
					value = integer_format % value
				else:
					value = integer_format(value)
			elif type(value) == float:
				if float_format_is_string:
					value = float_format % value
				else:
					value = float_format(value)

			new_dataframe[column].append(value)

	data_frame = DataFrame(
			{
				index.__str__(): [index.__str__()] + new_dataframe[index] for index, column in data_frame.items()
			}
	)

	columns_split = columns_split if columns_split is not None else ""
	right_border = right_border if right_border is not None else ""
	left_border = left_border if left_border is not None else ""

	size_of_columns = [len(max(column.tolist(), key=len)) for index, column in data_frame.items()]
	size_of_table = sum(size_of_columns) + len(columns_split) * (len(size_of_columns) - 1) + len(left_border) + len(right_border)

	for column, size_of_column in zip(data_frame.columns, size_of_columns):
		data_frame[column] = data_frame[column].apply(lambda value_: value_ + " " * (size_of_column - len(value_)))

	output_lines = [
		"%s%s%s" % (
				left_border,
				columns_split.join([column for column in row.values.tolist()]),
				right_border
		) for index, row in data_frame.iterrows()
	]

	if top_border is not None:
		output_lines.insert(0, top_border * size_of_table)

	if header_border is not None:
		output_lines.insert(2, header_border * size_of_table)

	if bottom_border is not None:
		output_lines.append(bottom_border * size_of_table)

	return "\n".join(output_lines)
