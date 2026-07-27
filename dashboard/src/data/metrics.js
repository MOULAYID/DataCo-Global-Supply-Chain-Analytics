/**
 * Data provider for DataCo Executive SaaS Dashboard.
 * Reads exported metrics from Python pipeline.
 */
import metricsData from '../../../data/processed/dashboard_metrics.json';

export const getMetrics = () => {
  return metricsData;
};

export default metricsData;
