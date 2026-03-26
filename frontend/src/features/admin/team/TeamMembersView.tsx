import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getTeamMembers, createTeamMember, updateTeamMember, deleteTeamMember } from '../../../api/teamMembers'
import { getUsers } from '../../../api/users'
import type { Team } from '../../../types/teams'
import type { TeamMember, TeamPosition } from '../../../types/teamMembers'
import AdminTable from '../AdminTable'
import Modal from '../../../components/ui/Modal'
import { MdArrowBack, MdEdit, MdDelete } from 'react-icons/md'

interface Props {
    team: Team
    onBack: () => void
}

const positionLabel: Record<TeamPosition, string> = {
    head: 'Руководитель',
    member: 'Сотрудник',
}

export default function TeamMembersView({ team, onBack }: Props) {
    const queryClient = useQueryClient()
    const [isOpen, setIsOpen] = useState(false)
    const [deleteId, setDeleteId] = useState<number | null>(null)
    const [editMember, setEditMember] = useState<TeamMember | null>(null)
    const [editPosition, setEditPosition] = useState<TeamPosition>('member')
    const [userId, setUserId] = useState<number | undefined>()
    const [position, setPosition] = useState<TeamPosition>('member')

    const { data: members, isLoading, isError } = useQuery({
        queryKey: ['team_members', team.id],
        queryFn: () => getTeamMembers(team.id)
    })

    const { data: users } = useQuery({ queryKey: ['users'], queryFn: getUsers })

    const invalidate = () => queryClient.invalidateQueries({ queryKey: ['team_members', team.id] })

    const addMutation = useMutation({
        mutationFn: createTeamMember,
        onSuccess: () => {
            invalidate()
            setIsOpen(false)
            setUserId(undefined)
            setPosition('member')
        }
    })

    const updateMutation = useMutation({
        mutationFn: ({ id, position }: { id: number; position: TeamPosition }) =>
            updateTeamMember(id, { team_position: position }),
        onSuccess: () => { invalidate(); setEditMember(null) }
    })

    const deleteMutation = useMutation({
        mutationFn: deleteTeamMember,
        onSuccess: () => { invalidate(); setDeleteId(null) }
    })

    const memberUserIds = new Set(members?.map(m => m.user_id))
    const availableUsers = users?.filter(u => !memberUserIds.has(u.id)) ?? []
    const userName = (id: number) => users?.find(u => u.id === id)?.fullname ?? `ID ${id}`

    const inputClass = "w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 outline-none focus:border-[#3D3FAA]"

    if (isLoading) return <div className="text-gray-500 text-sm p-4">Загрузка...</div>
    if (isError) return <div className="text-red-400 text-sm p-4">Ошибка загрузки</div>

    return (
        <div>
            <div className="flex items-center gap-3 mb-4">
                <button
                    onClick={onBack}
                    className="flex items-center gap-1 text-sm text-[#3D3FAA] hover:underline cursor-pointer"
                >
                    <MdArrowBack className="text-lg" /> Назад к командам
                </button>
                <span className="text-gray-300">|</span>
                <span className="text-gray-600 text-sm font-medium">{team.name}</span>
            </div>

            <AdminTable
                columns={['ID', 'Сотрудник', 'Роль', 'Действия']}
                headerContent={
                    <button
                        onClick={() => setIsOpen(true)}
                        className="px-4 py-1.5 rounded-lg text-sm font-medium bg-[#3D3FAA] text-white cursor-pointer"
                    >
                        Добавить участника
                    </button>
                }
                rows={members?.map(member => [
                    member.id,
                    userName(member.user_id),
                    positionLabel[member.team_position],
                    <div className="flex gap-2">
                        <button
                            onClick={() => { setEditMember(member); setEditPosition(member.team_position) }}
                            className="p-1.5 rounded hover:bg-gray-100 text-[#3D3FAA] cursor-pointer transition"
                            title="Изменить роль"
                        >
                            <MdEdit className="text-lg" />
                        </button>
                        <button
                            onClick={() => setDeleteId(member.id)}
                            className="p-1.5 rounded hover:bg-gray-100 text-red-400 cursor-pointer transition"
                            title="Удалить"
                        >
                            <MdDelete className="text-lg" />
                        </button>
                    </div>
                ]) ?? []}
            />

            <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Добавить участника">
                <div className="flex flex-col gap-4">
                    <div>
                        <label className="block text-sm text-gray-600 mb-1">Пользователь</label>
                        <select
                            value={userId ?? ''}
                            onChange={e => setUserId(e.target.value ? Number(e.target.value) : undefined)}
                            className={inputClass}
                        >
                            <option value="">— Выберите пользователя —</option>
                            {availableUsers.map(u => (
                                <option key={u.id} value={u.id}>{u.fullname}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm text-gray-600 mb-1">Роль в команде</label>
                        <select
                            value={position}
                            onChange={e => setPosition(e.target.value as TeamPosition)}
                            className={inputClass}
                        >
                            <option value="member">Сотрудник</option>
                            <option value="head">Руководитель</option>
                        </select>
                    </div>
                    <div className="flex justify-end gap-2">
                        <button onClick={() => setIsOpen(false)}
                            className="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 cursor-pointer">
                            Отмена
                        </button>
                        <button
                            onClick={() => userId && addMutation.mutate({ team_id: team.id, user_id: userId, team_position: position })}
                            disabled={!userId || addMutation.isPending}
                            className="px-4 py-2 text-sm bg-[#3D3FAA] text-white rounded-lg cursor-pointer disabled:opacity-50"
                        >
                            {addMutation.isPending ? 'Добавление...' : 'Добавить'}
                        </button>
                    </div>
                </div>
            </Modal>

            <Modal isOpen={!!editMember} onClose={() => setEditMember(null)} title="Изменить роль">
                <div className="flex flex-col gap-4">
                    <div>
                        <label className="block text-sm text-gray-600 mb-1">Роль в команде</label>
                        <select
                            value={editPosition}
                            onChange={e => setEditPosition(e.target.value as TeamPosition)}
                            className={inputClass}
                        >
                            <option value="member">Сотрудник</option>
                            <option value="head">Руководитель</option>
                        </select>
                    </div>
                    <div className="flex justify-end gap-2">
                        <button onClick={() => setEditMember(null)}
                            className="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 cursor-pointer">
                            Отмена
                        </button>
                        <button
                            onClick={() => updateMutation.mutate({ id: editMember!.id, position: editPosition })}
                            disabled={updateMutation.isPending}
                            className="px-4 py-2 text-sm bg-[#3D3FAA] text-white rounded-lg cursor-pointer disabled:opacity-50"
                        >
                            {updateMutation.isPending ? 'Сохранение...' : 'Сохранить'}
                        </button>
                    </div>
                </div>
            </Modal>

            <Modal isOpen={!!deleteId} onClose={() => setDeleteId(null)} title="Удалить участника">
                <p className="text-gray-600 text-sm mb-6">Вы уверены, что хотите удалить этого участника из команды?</p>
                <div className="flex justify-end gap-2">
                    <button onClick={() => setDeleteId(null)}
                        className="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 cursor-pointer">
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
        </div>
    )
}
