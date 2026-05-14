import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getTeamMembers, createTeamMember, deleteTeamMember } from '../../../api/teamMembers'
import { getUsers } from '../../../api/users'
import type { Team } from '../../../types/teams'
import type { TeamPosition } from '../../../types/teamMembers'
import Modal from '../../../components/ui/Modal'
import { MdDelete } from 'react-icons/md'

interface Props {
    team: Team
    onClose: () => void
}

const positionLabel: Record<TeamPosition, string> = {
    head: 'Руководитель',
    member: 'Участник',
}

export default function TeamMembersModal({ team, onClose }: Props) {
    const queryClient = useQueryClient()
    const [showAdd, setShowAdd] = useState(false)
    const [userId, setUserId] = useState<number | undefined>()
    const [position, setPosition] = useState<TeamPosition>('member')

    const { data: members, isLoading } = useQuery({
        queryKey: ['team_members', team.id],
        queryFn: () => getTeamMembers(team.id)
    })

    const { data: users } = useQuery({ queryKey: ['users'], queryFn: getUsers })

    const invalidate = () => queryClient.invalidateQueries({ queryKey: ['team_members', team.id] })

    const addMutation = useMutation({
        mutationFn: createTeamMember,
        onSuccess: () => { invalidate(); setShowAdd(false); setUserId(undefined); setPosition('member') }
    })

    const removeMutation = useMutation({
        mutationFn: deleteTeamMember,
        onSuccess: invalidate
    })

    const memberUserIds = new Set(members?.map(m => m.user_id))
    const availableUsers = users?.filter(u => !memberUserIds.has(u.id)) ?? []

    const userName = (userId: number) => users?.find(u => u.id === userId)?.fullname ?? `ID ${userId}`

    return (
        <Modal isOpen={true} onClose={onClose} title={`Участники: ${team.name}`}>
            {isLoading ? (
                <div className="text-gray-500 text-sm">Загрузка...</div>
            ) : (
                <div className="flex flex-col gap-3">
                    {members?.length === 0 && (
                        <p className="text-gray-400 text-sm">Участников пока нет</p>
                    )}
                    {members?.map(member => (
                        <div key={member.id} className="flex justify-between items-center border-b border-gray-100 pb-2">
                            <div>
                                <span className="text-sm text-gray-800">{userName(member.user_id)}</span>
                                <span className="ml-2 text-xs text-gray-400">{positionLabel[member.team_position]}</span>
                            </div>
                            <button
                                onClick={() => removeMutation.mutate(member.id)}
                                className="p-1.5 rounded hover:bg-gray-100 text-red-400 cursor-pointer transition"
                                title="Удалить"
                            >
                                <MdDelete className="text-lg" />
                            </button>
                        </div>
                    ))}

                    {showAdd ? (
                        <div className="flex flex-col gap-3 pt-2 border-t border-gray-100">
                            <div>
                                <label className="block text-sm text-gray-600 mb-1">Пользователь</label>
                                <select
                                    value={userId ?? ''}
                                    onChange={e => setUserId(e.target.value ? Number(e.target.value) : undefined)}
                                    className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 outline-none focus:border-[#3D3FAA]"
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
                                    className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 outline-none focus:border-[#3D3FAA]"
                                >
                                    <option value="member">Сотрудник</option>
                                    <option value="head">Руководитель</option>
                                </select>
                            </div>
                            <div className="flex justify-end gap-2">
                                <button onClick={() => setShowAdd(false)}
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
                    ) : (
                        <button
                            onClick={() => setShowAdd(true)}
                            className="mt-1 px-4 py-1.5 rounded-lg text-sm font-medium bg-[#3D3FAA] text-white cursor-pointer self-start"
                        >
                            Добавить участника
                        </button>
                    )}
                </div>
            )}
        </Modal>
    )
}
