import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getUsers, createUser, updateUser, deleteUser } from '../../../api/users'
import { getAgencies } from '../../../api/agencies'
import { getPositions } from '../../../api/positions'
import type { User, UserUpdate } from '../../../types/users'
import { MdEdit, MdDelete } from 'react-icons/md'
import AdminTable from '../AdminTable'
import Modal from '../../../components/ui/Modal'
import UserForm from './UserForm'

const userTypeLabel: Record<string, string> = {
    private: 'Частный',
    corporate: 'Корпоративный',
    supervisor: 'Руководитель',
}

export default function UsersTab() {
    const queryClient = useQueryClient()
    const [isOpen, setIsOpen] = useState(false)
    const [editUser, setEditUser] = useState<User | null>(null)
    const [deleteUser_, setDeleteUser] = useState<User | null>(null)

    const { data: users, isLoading, isError } = useQuery({ queryKey: ['users'], queryFn: getUsers })
    const { data: agencies } = useQuery({ queryKey: ['agencies'], queryFn: getAgencies })
    const { data: positions } = useQuery({ queryKey: ['positions'], queryFn: getPositions })

    const agencyName = (id: number | null) => agencies?.find(a => a.id === id)?.name ?? 'Нет данных'
    const positionName = (id: number | null) => positions?.find(p => p.id === id)?.name ?? 'Нет данных'

    const invalidate = () => queryClient.invalidateQueries({ queryKey: ['users'] })

    const createMutation = useMutation({
        mutationFn: createUser,
        onSuccess: () => { invalidate(); setIsOpen(false) }
    })

    const updateMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: UserUpdate }) => updateUser(id, data),
        onSuccess: () => { invalidate(); setEditUser(null) }
    })

    const deleteMutation = useMutation({
        mutationFn: deleteUser,
        onSuccess: () => { invalidate(); setDeleteUser(null) }
    })

    if (isLoading) return <div className="text-gray-500 text-sm p-4">Загрузка...</div>
    if (isError) return <div className="text-red-400 text-sm p-4">Ошибка загрузки</div>

    return (
        <>
            <AdminTable
                columns={['ID', 'Имя', 'Логин', 'Email', 'Тип', 'Агентство', 'Должность', 'IP', 'Активен', 'Суперадмин', 'В системе с', 'Действия']}
                headerContent={
                    <button onClick={() => setIsOpen(true)}
                        className="px-4 py-1.5 rounded-lg text-sm font-medium bg-[#3D3FAA] text-white cursor-pointer">
                        Добавить
                    </button>
                }
                rows={users?.slice().sort((a, b) => a.id - b.id).map(user => [
                    user.id,
                    user.fullname,
                    user.login,
                    user.email,
                    userTypeLabel[user.user_type] ?? user.user_type,
                    agencyName(user.agency_id),
                    positionName(user.position_id),
                    user.ip_address ?? 'Нет данных',
                    user.is_active ? 'Да' : 'Нет',
                    user.is_superuser ? 'Да' : 'Нет',
                    new Date(user.created_at).toLocaleDateString('ru-RU'),
                    <div className="flex gap-2">
                        <button onClick={() => setEditUser(user)}
                            className="p-1.5 rounded hover:bg-gray-100 text-[#3D3FAA] cursor-pointer transition"
                            title="Изменить">
                            <MdEdit className="text-lg" />
                        </button>
                        <button onClick={() => setDeleteUser(user)}
                            className="p-1.5 rounded hover:bg-gray-100 text-red-400 cursor-pointer transition"
                            title="Удалить">
                            <MdDelete className="text-lg" />
                        </button>
                    </div>
                ]) ?? []}
            />

            <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Добавить пользователя">
                <UserForm
                    mode="create"
                    onSubmit={(data) => createMutation.mutate(data)}
                    onClose={() => setIsOpen(false)}
                    isPending={createMutation.isPending}
                />
            </Modal>

            <Modal isOpen={!!editUser} onClose={() => setEditUser(null)} title="Изменить пользователя">
                <UserForm
                    mode="edit"
                    defaultValue={{
                        fullname: editUser?.fullname ?? '',
                        email: editUser?.email,
                        login: editUser?.login,
                        user_type: editUser?.user_type,
                        agency_id: editUser?.agency_id ?? undefined,
                        position_id: editUser?.position_id ?? undefined,
                        ip_address: editUser?.ip_address ?? undefined,
                        is_active: editUser?.is_active,
                    }}
                    onSubmit={(data) => updateMutation.mutate({ id: editUser!.id, data })}
                    onClose={() => setEditUser(null)}
                    isPending={updateMutation.isPending}
                />
            </Modal>

            <Modal isOpen={!!deleteUser_} onClose={() => setDeleteUser(null)} title="Удалить пользователя">
                <p className="text-gray-600 text-sm mb-2">
                    Вы уверены, что хотите удалить пользователя <span className="font-medium">{deleteUser_?.fullname}</span>?
                </p>
                <p className="text-gray-400 text-xs mb-6">Это действие нельзя отменить.</p>
                <div className="flex justify-end gap-2">
                    <button onClick={() => setDeleteUser(null)}
                        className="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 cursor-pointer">
                        Отмена
                    </button>
                    <button
                        onClick={() => deleteMutation.mutate(deleteUser_!.id)}
                        disabled={deleteMutation.isPending}
                        className="px-4 py-2 text-sm bg-red-500 text-white rounded-lg cursor-pointer disabled:opacity-50">
                        {deleteMutation.isPending ? 'Удаление...' : 'Удалить'}
                    </button>
                </div>
            </Modal>
        </>
    )
}
