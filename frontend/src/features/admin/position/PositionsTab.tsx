import { useState } from "react"
import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query"
import { createPosition, getPositions, deletePosition } from "../../../api/positions"
import Modal from "../../../components/ui/Modal"
import PositionForm from "./PositionForm" 
import AdminTable from "../AdminTable"
import { MdDelete } from 'react-icons/md'

export default function PositionTab() {
    const queryClient = useQueryClient()
    const [isOpen, setIsOpen] = useState(false)
    const [deleteId, setDeleteId] = useState<number | null>(null)

    const {data: positions, isLoading, isError } = useQuery({
        queryKey: ['positions'],
        queryFn: getPositions
    })

    const invalidate = () => queryClient.invalidateQueries({ queryKey: ['positions']})

    const createMutation = useMutation({
        mutationFn: createPosition,
        onSuccess: () => {invalidate(); setIsOpen(false)}
    })
    
    const deleteMutation = useMutation({
        mutationFn: deletePosition,
        onSuccess: () => {invalidate(); setDeleteId(null)}
    })

    if (isLoading) return <div className="text-gray-500 text-sm p-4">Загрузка...</div>
    if (isError) return <div className="text-red-400 text-sm p-4">Ошибка загрузки</div>

    return(
        <>
            <AdminTable 
                columns={["ID", "Название", "Действия"]}
                headerContent={
                    <button 
                        onClick={ () => setIsOpen(true) }
                        className="px-4 py-1.5 rounded-lg text-sm font-medium bg-[#3D3FAA] text-white cursor-pointer"
                     >Добавить</button>   
                }
                rows={positions?.map(position => [
                    position.id,
                    position.name,
                    <button onClick={() => setDeleteId(position.id)}
                        className="p-1.5 rounded hover:bg-gray-100 text-red-400 cursor-pointer transition"
                        title="Удалить">
                        <MdDelete className="text-lg" />
                    </button>    
                ]) ?? []}
            />

            <Modal 
                isOpen={isOpen}
                onClose={() => setIsOpen(false)}
                title="Добавить должность"
            >
                <PositionForm
                    onSubmit={(name) => createMutation.mutate({name})}
                    onClose={() => setIsOpen(false)}
                    isPending={createMutation.isPending}
                />
            </Modal>  

            <Modal 
                isOpen={!!deleteId}
                onClose={() => setDeleteId(null)}
                title="Удалить должность"
            >
                <p className="text-gray-600 text-sm mb-6">
                    Вы уверены, что хотите удалить должность?
                </p>
                <div className="flex justify-end gap-2">
                    <button 
                        onClick={() => setDeleteId(null)}
                        className="px-4 py-2 text-sm text-gray-500 cursor-pointer"
                    >
                        Отмена
                    </button> 
                    <button 
                        onClick={() => deleteMutation.mutate(deleteId!)}
                        disabled={deleteMutation.isPending}
                        className="px-4 py-2 text-sm bg-red-500 text-white rounded-lg cursor-pointer disabled:opacity-50"
                    >
                        {deleteMutation.isPending ? 'Удаление...' : 'Удалить'}
                    </button>
                </div>
            </Modal>
                        
        </>
    )
}
