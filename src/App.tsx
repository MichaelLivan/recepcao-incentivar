import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'sonner'
import { AuthProvider } from './contexts/AuthContext'
import { ThemeProvider } from './components/theme-provider'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import SalasPage from './pages/SalasPage'
import EstoquePage from './pages/EstoquePage'
import OrcamentosPage from './pages/OrcamentosPage'
import BrindesPage from './pages/BrindesPage'
import ListaEsperaPage from './pages/ListaEsperaPage'
import VisitasPage from './pages/VisitasPage'
import AnamnesesPage from './pages/AnamnesesPage'
import ProtectedRoute from './components/ProtectedRoute'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="light" storageKey="reception-sync-theme">
        <AuthProvider>
          <Router>
            <div className="min-h-screen bg-background">
              <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <DashboardPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/salas"
                  element={
                    <ProtectedRoute>
                      <SalasPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/estoque"
                  element={
                    <ProtectedRoute requiredReception="103">
                      <EstoquePage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/orcamentos"
                  element={
                    <ProtectedRoute requiredReceptions={['103', '808', '108', '203', '1009', '1108']}>
                      <OrcamentosPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/brindes"
                  element={
                    <ProtectedRoute requiredReceptions={['103', '808', '108', '203', '1009', '1108', '1002']}>
                      <BrindesPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/lista-espera"
                  element={
                    <ProtectedRoute requiredReception="1002">
                      <ListaEsperaPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/visitas"
                  element={
                    <ProtectedRoute requiredReception="108">
                      <VisitasPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/anamneses"
                  element={
                    <ProtectedRoute requiredReception="808">
                      <AnamnesesPage />
                    </ProtectedRoute>
                  }
                />
              </Routes>
              <Toaster />
            </div>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App