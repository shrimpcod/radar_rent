import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import ProtectedRouter from "./ProtectedRouter"
import LoginPage from '../pages/LoginPage'
import ListingsPage from '../pages/ListingsPage'
import AppLayout from "../components/layout/AppLayout"
import ProfilePage from "../pages/ProfilePage"

export default function Router(){
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<LoginPage />}/>
                <Route element={
                    <ProtectedRouter>
                        <AppLayout/>
                    </ProtectedRouter>
                }>  
                    <Route path="/profile" element={<ProfilePage />} />
                    <Route path="/listings" element={<ListingsPage />} />
                    <Route path="/my_objects" element={<div>Объекты в работе</div>} />
                    <Route path="/clients" element={<div>База клиентов</div>} />
                    <Route path="/schedule" element={<div>График</div>} />
                </Route>
                
                <Route path="*" element={<Navigate to="/listings" />} />
            </Routes>
        </BrowserRouter>
    )
}