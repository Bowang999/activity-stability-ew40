import unittest
import numpy as np
from activity_stability import activity_stability, ew_std, turnover_cv, process_cross_section, hac_mean, adjust_p, performance


class EstimatorTests(unittest.TestCase):
    def test_literal_weights_gaps_and_prefix(self):
        x = np.exp(np.random.default_rng(17).normal(size=(150, 3)))
        x[65, 1] = np.nan
        actual = ew_std(x)
        np.testing.assert_allclose(actual[:100], ew_std(x[:100]), equal_nan=True)
        for j in range(3):
            start = 0
            for t in range(len(x)):
                if not np.isfinite(x[t, j]):
                    start = t+1
                    continue
                if t-start+1 < 40:
                    self.assertTrue(np.isnan(actual[t, j]))
                    continue
                v = x[start:t+1, j]; w = (39/41)**np.arange(len(v)-1, -1, -1); w /= w.sum()
                expected = np.sqrt((w @ (v-w@v)**2)/(1-w@w))
                self.assertAlmostEqual(actual[t, j], expected, places=11)

    def test_reference_excludes_today_and_unit_invariance(self):
        x = np.exp(np.random.default_rng(19).normal(8, .2, (160, 3)))
        raw = activity_stability(x)
        np.testing.assert_allclose(raw, activity_stability(x*np.array([1, 7, 100])), equal_nan=True, atol=1e-11)
        self.assertTrue(np.isnan(raw[:59]).all())
        self.assertTrue(np.isfinite(raw[59:]).all())
        ra = np.full_like(x, np.nan)
        for t in range(20, len(x)):
            ra[t] = x[t]/x[t-20:t].mean(0)
        np.testing.assert_allclose(raw, ew_std(ra), equal_nan=True, atol=1e-11)

    def test_cv_literal_and_zero_turnover(self):
        x = np.exp(np.random.default_rng(22).normal(-3, .4, (100, 2))); x[50, 0] = 0.
        actual = turnover_cv(x)
        for t in range(19, 100):
            v = x[t-19:t+1]
            np.testing.assert_allclose(actual[t], v.std(0, ddof=1)/v.mean(0), atol=1e-12)
        actual = turnover_cv(x, 40, ew=True)
        for t in range(39, 100):
            w = (39/41)**np.arange(t, -1, -1); w /= w.sum(); v = x[:t+1]; mu = w@v
            expected = np.sqrt(w @ ((v-mu)**2)/(1-w@w))/mu
            np.testing.assert_allclose(actual[t], expected, atol=1e-12)

    def test_joint_projection_duplicate_controls(self):
        rng = np.random.default_rng(25); n = 180
        cap = np.exp(rng.normal(20, 1, n)); groups = np.repeat([0, 1, 2], 60)
        control = rng.normal(size=n); raw = .7*control + rng.normal(size=n)
        score = process_cross_section(raw, cap, groups, controls=np.column_stack([control, control]))
        self.assertAlmostEqual(score.std(), 1.)
        for g in range(3):
            self.assertAlmostEqual(score[groups == g].mean(), 0.)
        self.assertAlmostEqual(float(score@control), 0., places=9)
        self.assertAlmostEqual(float(score@np.log(cap)), 0., places=8)


class StatisticsTests(unittest.TestCase):
    def test_hac_matrix_reference(self):
        x = np.random.default_rng(28).normal(.1, 1, 150); lag = 12
        z = x-x.mean(); d = np.abs(np.arange(len(x))[:, None]-np.arange(len(x)))
        weights = np.maximum(0., 1-d/(lag+1))
        expected = np.sqrt(z @ weights @ z / len(x)**2)
        self.assertAlmostEqual(hac_mean(x, lag)["se"], expected)

    def test_by_literal_sorted_formula(self):
        p = np.array([.004, .8, .02, .004, 1.]); order = np.argsort(p); m = len(p)
        scaled = p[order]*m*np.sum(1/np.arange(1,m+1))/np.arange(1,m+1)
        expected = np.empty(m)
        for i in range(m):
            expected[order[i]] = min(1., min(scaled[i:]))
        np.testing.assert_allclose(adjust_p(p), expected)

    def test_initial_nav_in_drawdown(self):
        self.assertAlmostEqual(performance([-.1, .01])["max_drawdown_pct"], 10.)


if __name__ == "__main__":
    unittest.main()
