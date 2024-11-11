import numpy as np
import astropy.units as u
from astropy.constants import c, k_B
from astropy.coordinates import EarthLocation, AltAz, TEME, angular_separation
import satastro


### LINK BUDGET ###

def free_space_path_loss(distance, frequency):
    """Calculate the free space path loss for a given distance and frequency.

    Parameters
    ----------
    distance : Quantity
        Distance between transmitter and receiver.
    frequency : Quantity
        Frequency of the signal.

    Returns
    -------
    Quantity
        Free space path loss (dB)."""
    return 20*np.log10((4*np.pi*distance*frequency/c).to_value(u.dimensionless_unscaled))*u.dB

def gain(pointing, sat_pointing, 
         profile_receiver,
         noise_gain=0*u.dB, noise_pos=0*u.deg, 
         freq=10*u.GHz,
         emitter_gain=0*u.dB,
         data_rate=1*u.Mbit/u.s,
         sys_temp=150*u.K):
    """
    Gain function of the receiver with noise

    Parameters
    ----------
    pointing : AltAz
        The pointing of the antenna.
    sat_pointing : AltAz
        The pointing of the satellite.
    profile_receiver : pd.DataFrame (theta, gain)
        The receiver radiation profile.
    noise_gain : Quantity (default=0*u.dB)
        The noise on the gain.
    noise_pos : Quantity (default=0*u.deg)
        The noise on the pointing.
    freq : Quantity (default=10*u.GHz)
        The frequency of the signal.
    emitter_gain : Quantity (default=0*u.dB)
        The gain of the emitter.
    data_rate : Quantity (default=1*u.Mbit/u.s)
        The data rate.
    sys_temp : Quantity (default=150*u.K)
        The system noise temperature.
        
    Returns
    -------
    gain : Quantity
        The gain of the link
    """
    if noise_pos!=0*u.deg:
        noise_x = np.random.normal(0, noise_pos.to_value(u.deg), pointing.shape)*u.deg
        noise_y = np.random.normal(0, noise_pos.to_value(u.deg), pointing.shape)*u.deg
        pointing = altaz_add_offset(pointing, noise_x, noise_y)
    distance = np.rad2deg(angular_separation(pointing.az.to_value(u.rad), pointing.alt.to_value(u.rad), 
                                             sat_pointing.az.to_value(u.rad), sat_pointing.alt.to_value(u.rad)))
    gain = np.interp(distance, profile_receiver['theta'], profile_receiver['gain'])*u.dB
    if noise_gain!=0*u.dB:
        gain += np.random.normal(0, noise_gain.to_value(u.dB), gain.shape)*u.dB
    # Free space path loss
    gain -= free_space_path_loss(sat_pointing.distance, freq)
    # Emitter gain
    gain += emitter_gain
    # Noise temperature
    noise = 10*np.log10((k_B*sys_temp*data_rate/u.bit).to_value(u.W))*u.dB
    gain -= noise
    return gain


### ANGLES UTILS ###

def altaz_add_offset(altaz, angle_offset_x, angle_offset_y):
    """
    Add an angle offset to an AltAz object
    
    Parameters
    ----------
    altaz : AltAz
        The AltAz object
    angle_offset_x : Quantity
        The angle offset to add
    angle_offset_y : Quantity
        The angle offset to add
        
    Returns
    -------
    altaz : AltAz
        The AltAz object with the added angle
    """
    alt, az = altaz.alt.to_value(u.rad), altaz.az.to_value(u.rad)
    az += angle_offset_x.to_value(u.rad)/np.cos(alt)
    alt += angle_offset_y.to_value(u.rad)
    # Careful near pole -> Better control : az in [0, 180]°, alt in [0, 180]°
    pole_change = alt>0.5*np.pi
    try:
        alt[pole_change] -= np.pi
        az[pole_change] += np.pi
    except:
        if pole_change:
            alt -= np.pi
            az += np.pi
    return AltAz(alt=alt*u.rad, az=az*u.rad, obstime=altaz.obstime, location=altaz.location)

def spiral_points(radius, r_spacing, points_spacing):
    """
    Generate spiral points
    
    Parameters
    ----------
    radius : float
        Max radius of spiral
    r_spacing : float
        Radial spacing
    points_spacing : float
        Points spacing
        
    Returns
    -------
    points : np.array
        The spiral points
    """
    points = [(0,0)]
    angle = points_spacing/r_spacing*2*np.pi
    r = r_spacing*angle/(2*np.pi)
    # Better sampling around center
    for i in np.arange(np.pi/3+angle,2*np.pi+angle,np.pi/3):
        x = points_spacing*np.cos(i)*np.sqrt((i-angle)/(2*np.pi))
        y = points_spacing*np.sin(i)*np.sqrt((i-angle)/(2*np.pi))
        points.append([x, y])
    # Archimedes spiral
    while r < radius:
        r = r_spacing*angle/(2*np.pi)
        x = r*np.cos(angle)
        y = r*np.sin(angle)
        points.append([x, y])
        angle += points_spacing/r
    return np.array(points)