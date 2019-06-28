from astroquery.gaia import Gaia

job = Gaia.launch_job_async("SELECT TOP 100 * FROM gaiadr2.gaia_source WHERE (parallax >= 0.1) \
AND radial_velocity != 'nan' \
AND astrometric_excess_noise_sig < 2", 
dump_to_file=True, output_format='fits', output_file='gaiadr2_top100_100pc.fits')

