import type { ReactNode } from "react";
import { MdClose } from "react-icons/md";

interface Props {
    isOpen: boolean
    onClose: () => void
    title: string
    children: ReactNode
}

export default function Modal({ isOpen, onClose, title, children }: Props) {
    if (!isOpen) return null

    return(
        <div 
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
            onClick={onClose}
        >
            <div 
                className="bg-white rounded-xl shadow-lg p-6 w-full max-w-md"
                onClick={e => e.stopPropagation()}
            >
                <div className="flex justify-between items-center mb-4">
                    <h2 className="text-lg font-semibold text-gray-800">{title}</h2>
                    <MdClose onClick={onClose} className="text-xl text-gray-400 hover:text-gray-600 cursor-pointer"/>
                </div>
                <div>
                    {children}
                </div>
            </div>
        </div>
    )
}