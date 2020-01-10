function loc (df, rows, cols) {
	if (rows === true) { rows = Object.keys(df) }
	if (cols === true && Object.keys(df).length > 0) { cols = Object.keys(Object.values(df)[0]) }
	if (!Array.isArray(rows)) { rows = [rows] }
	if (!Array.isArray(cols)) { cols = [cols] }
	const selectedRows = {}
	Object.entries(df).forEach((pr) => {
		const selectedCols = {}
		if (rows.includes(pr[0])) {
			Object.entries(pr[1]).forEach((pc) => {
				if (cols.includes(pc[0])) {
					selectedCols[pc[0]] = pc[1]
				}
			})
			selectedRows[pr[0]] = selectedCols
		}
	})
	return selectedRows
}

function getRow (df, row, cols) {
	return loc(df, row, cols)[row]
}

function getCol (df, rows, col) {
	const column = {}
	Object.entries(loc(df, rows, col)).forEach((p, i) => {
		column[i] = p[1][col]
	})
	return column
}

export { loc, getRow, getCol }
