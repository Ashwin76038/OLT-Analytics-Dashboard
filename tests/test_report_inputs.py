"""Guard the published report against stale CSV copies and date disclosure."""
import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

class ReportInputTests(unittest.TestCase):
    def test_dashboard_inputs_equal_public_model(self):
        for source in (ROOT/'data/powerbi_star_schema').glob('*.csv'):
            pd.testing.assert_frame_equal(pd.read_csv(source), pd.read_csv(ROOT/'dashboard/OLT_Service_Project/data'/source.name))

    def test_no_activation_relationship_or_published_dates(self):
        project=ROOT/'dashboard/OLT_Service_Project'
        relationships=(project/'OLT.SemanticModel/definition/relationships.tmdl').read_text()
        self.assertNotIn('activation_date_key', relationships)
        f=pd.read_csv(project/'data/fact_customer_service.csv')
        for c in ['activation_date_key','reported_activation_date_key','valid_tenure_days','valid_tenure_months']:
            self.assertTrue(f[c].isna().all(), c)
