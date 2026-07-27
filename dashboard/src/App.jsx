import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import ExecutiveSummary from './pages/ExecutiveSummary';
import SalesAnalytics from './pages/SalesAnalytics';
import ProfitabilityPage from './pages/ProfitabilityPage';
import CustomerAnalytics from './pages/CustomerAnalytics';
import ProductAnalytics from './pages/ProductAnalytics';
import ShippingAnalytics from './pages/ShippingAnalytics';
import GeographyAnalytics from './pages/GeographyAnalytics';
import InventoryAnalytics from './pages/InventoryAnalytics';
import FraudAnalytics from './pages/FraudAnalytics';
import ForecastingPage from './pages/ForecastingPage';
import KpiScorecard from './pages/KpiScorecard';
import metricsData from './data/metrics';

export default function App() {
  const [activePage, setActivePage] = useState('executive');
  const [darkMode, setDarkMode] = useState(true);
  const [metrics, setMetrics] = useState(metricsData);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const renderContent = () => {
    switch (activePage) {
      case 'executive': return <ExecutiveSummary metrics={metrics} />;
      case 'sales': return <SalesAnalytics metrics={metrics} />;
      case 'profitability': return <ProfitabilityPage metrics={metrics} />;
      case 'customers': return <CustomerAnalytics metrics={metrics} />;
      case 'products': return <ProductAnalytics metrics={metrics} />;
      case 'shipping': return <ShippingAnalytics metrics={metrics} />;
      case 'geography': return <GeographyAnalytics metrics={metrics} />;
      case 'inventory': return <InventoryAnalytics metrics={metrics} />;
      case 'fraud': return <FraudAnalytics metrics={metrics} />;
      case 'forecasting': return <ForecastingPage metrics={metrics} />;
      case 'kpi': return <KpiScorecard metrics={metrics} />;
      default: return <ExecutiveSummary metrics={metrics} />;
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg-main)] text-[var(--text-main)] flex flex-col font-sans transition-colors duration-300">
      <Navbar darkMode={darkMode} setDarkMode={setDarkMode} activePage={activePage} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar activePage={activePage} setActivePage={setActivePage} />
        <main className="flex-1 p-8 overflow-y-auto max-w-7xl mx-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}
