interface Props {
    columns: string[]
    rows: React.ReactNode[][]
    headerContent?: React.ReactNode
}

export default function AdminTable({ columns, rows, headerContent }: Props){
    return(
        <div className="bg-white rounded-xl shadow-sm">
            {headerContent && (
                    <div className="flex gap-2 p-4 border-b border-gray-100">
                        {headerContent}
                    </div>
                )}
            <table className="w-full">
                <thead>
                    <tr className="text-left text-xs text-gray-400 uppercase">
                        {columns.map( col => (
                            <th key={col} className="px-4 py-3">{col}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {rows.map((row, i) => (
                        <tr key={i} className="border-t border-gray-100 hover:bg-gray-50 text-sm text-gray-700">
                            {row.map((cell, j) => (
                                <td key={j} className="px-4 py-3">{cell}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}