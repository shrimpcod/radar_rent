import { useState } from 'react'

interface Props {
    defaultValue?: string
    onSubmit: (name: string) => void
    onClose: () => void
    isPending?: boolean
}

export default function AgencyForm({ defaultValue = "", onSubmit, onClose, isPending}: Props) {
    const [ name, setName ] = useState(defaultValue)

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        onSubmit(name)
    }

    return(
        <form onSubmit={handleSubmit} className='flex flex-col gap-4'>
            <div>
                <label className='block text-sm text-gray-600 mb-1'>Название</label>
                <input 
                    type="text"
                    value={name}
                    onChange={e => setName(e.target.value)}
                    className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 outline-none focus:border-[#3D3FAA]"
                    placeholder="Введите название агентства"
                    required
                />
            </div>
            <div className='flex justify-end gap-2'>
                <button
                    type="button"
                    onClick={onClose}
                    className="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 cursor-pointer"
                >Отмена</button>
                <button
                    type='submit'
                    disabled={isPending}
                    className="px-4 py-2 text-sm bg-[#3D3FAA] text-white rounded-lg cursor-pointer disabled:opacity-50" 
                >
                    {isPending ? 'Сохранение...' : 'Сохранить'}
                </button>
            </div>
        </form>
    )
}