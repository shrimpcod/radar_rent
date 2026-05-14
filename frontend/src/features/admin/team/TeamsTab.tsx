import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getTeams, createTeam, updateTeam, deleteTeam } from '../../../api/teams'
import { getAgencies } from '../../../api/agencies'
import type { Team } from '../../../types/teams'
import AdminTable from '../AdminTable'
import Modal from '../../../components/ui/Modal'
import TeamForm from './TeamForm'
import TeamMembersView from './TeamMembersView'
import { MdEdit, MdDelete, MdPeople } from 'react-icons/md'

export default function TeamsTab() {
    const queryClient = useQueryClient()
    const [isOpen, setIsOpen] = useState(false)
    const [editTeam, setEditTeam] = useState<Team | null>(null)
    const [deleteId, setDeleteId] = useState<number | null>(null)
    const [membersTeam, setMembersTeam] = useState<Team | null>(null)

    const { data: teams, isLoading, isError } = useQuery({ queryKey: ['teams'], queryFn: getTeams })
    const { data: agencies } = useQuery({ queryKey: ['agencies'], queryFn: getAgencies })

    const agencyName = (id: number) => agencies?.find(a => a.id === id)?.name ?? 'Нет данных'

    const invalidate = () => queryClient.invalidateQueries({ queryKey: ['teams'] })

    const createMutation = useMutation({
        mutationFn: createTeam,
        onSuccess: () => { invalidate(); setIsOpen(false) }
    })

    const updateMutation = useMutation({
        mutationFn: ({ id, name }: { id: number; name: string }) => updateTeam(id, { name }),
        onSuccess: () => { invalidate(); setEditTeam(null) }
    })

    const deleteMutation = useMutation({
        mutationFn: deleteTeam,
        onSuccess: () => { invalidate(); setDeleteId(null) }
    })

    if (membersTeam) return <TeamMembersView team={membersTeam} onBack={() => setMembersTeam(null)} />

    if (isLoading) return <div className="text-gray-500 text-sm p-4">Загрузка...</div>
    if (isError) return <div className="text-red-400 text-sm p-4">Ошибка загрузки</div>

    return (
        <>
            <AdminTable
                columns={['ID', 'Название', 'Агентство', 'Действия']}
                headerContent={
                    <button onClick={() => setIsOpen(true)}
                        className="px-4 py-1.5 rounded-lg text-sm font-medium bg-[#3D3FAA] text-white cursor-pointer">
                        Добавить
                    </button>
                }
                rows={teams?.slice().sort((a, b) => a.id - b.id).map(team => [
                    team.id,
                    team.name,
                    agencyName(team.agency_id),
                    <div className="flex gap-2">
                        <button onClick={() => setMembersTeam(team)}
                            className="p-1.5 rounded hover:bg-gray-100 text-gray-500 cursor-pointer transition"
                            title="Участники">
                            <MdPeople className="text-lg" />
                        </button>
                        <button onClick={() => setEditTeam(team)}
                            className="p-1.5 rounded hover:bg-gray-100 text-[#3D3FAA] cursor-pointer transition"
                            title="Изменить">
                            <MdEdit className="text-lg" />
                        </button>
                        <button onClick={() => setDeleteId(team.id)}
                            className="p-1.5 rounded hover:bg-gray-100 text-red-400 cursor-pointer transition"
                            title="Удалить">
                            <MdDelete className="text-lg" />
                        </button>
                    </div>
                ]) ?? []}
            />

            <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Добавить команду">
                <TeamForm
                    mode="create"
                    onSubmit={(data) => createMutation.mutate(data)}
                    onClose={() => setIsOpen(false)}
                    isPending={createMutation.isPending}
                />
            </Modal>

            <Modal isOpen={!!editTeam} onClose={() => setEditTeam(null)} title="Изменить команду">
                <TeamForm
                    mode="edit"
                    defaultValue={{ name: editTeam?.name ?? '', agency_id: editTeam?.agency_id ?? 0 }}
                    onSubmit={(data) => updateMutation.mutate({ id: editTeam!.id, name: data.name ?? '' })}
                    onClose={() => setEditTeam(null)}
                    isPending={updateMutation.isPending}
                />
            </Modal>

            <Modal isOpen={!!deleteId} onClose={() => setDeleteId(null)} title="Удалить команду">
                <p className="text-gray-600 text-sm mb-6">Вы уверены, что хотите удалить эту команду? Это действие нельзя отменить.</p>
                <div className="flex justify-end gap-2">
                    <button onClick={() => setDeleteId(null)}
                        className="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 cursor-pointer">
                        Отмена
                    </button>
                    <button
                        onClick={() => deleteMutation.mutate(deleteId!)}
                        disabled={deleteMutation.isPending}
                        className="px-4 py-2 text-sm bg-red-500 text-white rounded-lg cursor-pointer disabled:opacity-50">
                        {deleteMutation.isPending ? 'Удаление...' : 'Удалить'}
                    </button>
                </div>
            </Modal>

        </>
    )
}
