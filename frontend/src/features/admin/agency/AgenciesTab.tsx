import { useState } from "react";
import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";
import { createAgency, getAgencies, updateAgency, deleteAgency } from "../../../api/agencies"
import type { Agency } from "../../../types/agency"
import { MdEdit, MdDelete } from 'react-icons/md'
import Modal from "../../../components/ui/Modal"
import AgencyForm from "./AgencyForm"
import AdminTable from "../AdminTable";

export default function AgenciesTab() {
    const queryClient = useQueryClient()
    const [isOpen, setIsOpen] = useState(false)
    const [editAgency, setEditAgency] = useState<Agency | null>(null)
    const [deleteId, setDeleteId] = useState<number | null>(null)

    const {data: agencies, isLoading, isError } = useQuery({
        queryKey: ['agencies'],
        queryFn: getAgencies
    })

    const invalidate = () => queryClient.invalidateQueries({ queryKey: ['agencies'] })

    const createMutation = useMutation({
        mutationFn: createAgency,
        onSuccess: () => { invalidate(); setIsOpen(false) }
    })

    const updateMutation = useMutation({
        mutationFn: ({ id, name }: { id: number; name: string }) => updateAgency(id, { name }),
        onSuccess: () => { invalidate(); setEditAgency(null) }
    })

    const deleteMutation = useMutation({
        mutationFn: deleteAgency,
        onSuccess: () => { invalidate(); setDeleteId(null) }
    })


    if (isLoading) return <div className="text-gray-500 text-sm p-4">Загрузка...</div>
    if (isError) return <div className="text-red-400 text-sm p-4">Ошибка загрузки</div>

    return (
        <>
            <AdminTable
                columns={["ID", "Название", "Действия"]}
                headerContent={
                    <button
                        onClick={() => setIsOpen(true)}
                        className="px-4 py-1.5 rounded-lg text-sm font-medium transition-colors bg-[#3D3FAA] text-white cursor-pointer"
                    >
                        Добавить
                    </button>
                }
                rows={agencies?.map(agency => [
                    agency.id,
                    agency.name,
                    <div className="flex gap-2">
                        <button onClick={() => setEditAgency(agency)}
                            className="p-1.5 rounded hover:bg-gray-100 text-[#3D3FAA] cursor-pointer transition"
                            title="Изменить">
                            <MdEdit className="text-lg" />
                        </button>
                        <button onClick={() => setDeleteId(agency.id)}
                            className="p-1.5 rounded hover:bg-gray-100 text-red-400 cursor-pointer transition"
                            title="Удалить">
                            <MdDelete className="text-lg" />
                        </button>
                    </div> 
                ]) ?? []}
            /> 
            <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Добавить агентство">
                <AgencyForm
                    onSubmit={(name) => createMutation.mutate({ name })}
                    onClose={() => setIsOpen(false)}
                    isPending={createMutation.isPending}
                />
            </Modal>

            <Modal isOpen={!!deleteId} onClose={() => setDeleteId(null)} title="Удалить агентство">
                <p className="text-gray-600 text-sm mb-6">Вы уверены, что хотите удалить это агентство? Это действие нельзя отменить.</p>
                <div className="flex justify-end gap-2">
                    <button
                        onClick={() => setDeleteId(null)}
                        className="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 cursor-pointer"
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

            <Modal isOpen={!!editAgency} onClose={() => setEditAgency(null)} title="Изменить агентство">
                <AgencyForm
                    defaultValue={editAgency?.name}
                    onSubmit={(name) => updateMutation.mutate({ id: editAgency!.id, name })}
                    onClose={() => setEditAgency(null)}
                    isPending={updateMutation.isPending}
                />
            </Modal>
        </>
    )
}