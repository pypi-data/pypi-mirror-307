use nalgebra::DVector;
use num::Complex;

use crate::{
    amplitudes::{AmplitudeID, ParameterLike},
    data::Event,
    resources::{Cache, ParameterID, Parameters, Resources},
    Float, LadduError,
};

use super::Amplitude;

/// A scalar-valued [`Amplitude`] which just contains a single parameter as its value.
#[derive(Clone)]
pub struct Scalar {
    name: String,
    value: ParameterLike,
    pid: ParameterID,
}

impl Scalar {
    /// Create a new [`Scalar`] with the given name and parameter value.
    pub fn new(name: &str, value: ParameterLike) -> Box<Self> {
        Self {
            name: name.to_string(),
            value,
            pid: Default::default(),
        }
        .into()
    }
}

impl Amplitude for Scalar {
    fn register(&mut self, resources: &mut Resources) -> Result<AmplitudeID, LadduError> {
        self.pid = resources.register_parameter(&self.value);
        resources.register_amplitude(&self.name)
    }

    fn compute(&self, parameters: &Parameters, _event: &Event, _cache: &Cache) -> Complex<Float> {
        Complex::new(parameters.get(self.pid), 0.0)
    }

    fn compute_gradient(
        &self,
        _parameters: &Parameters,
        _event: &Event,
        _cache: &Cache,
        gradient: &mut DVector<Complex<Float>>,
    ) {
        if let ParameterID::Parameter(ind) = self.pid {
            gradient[ind] = Complex::ONE;
        }
    }
}

/// A complex-valued [`Amplitude`] which just contains two parameters representing its real and
/// imaginary parts.
#[derive(Clone)]
pub struct ComplexScalar {
    name: String,
    re: ParameterLike,
    pid_re: ParameterID,
    im: ParameterLike,
    pid_im: ParameterID,
}

impl ComplexScalar {
    /// Create a new [`ComplexScalar`] with the given name, real, and imaginary part.
    pub fn new(name: &str, re: ParameterLike, im: ParameterLike) -> Box<Self> {
        Self {
            name: name.to_string(),
            re,
            pid_re: Default::default(),
            im,
            pid_im: Default::default(),
        }
        .into()
    }
}

impl Amplitude for ComplexScalar {
    fn register(&mut self, resources: &mut Resources) -> Result<AmplitudeID, LadduError> {
        self.pid_re = resources.register_parameter(&self.re);
        self.pid_im = resources.register_parameter(&self.im);
        resources.register_amplitude(&self.name)
    }

    fn compute(&self, parameters: &Parameters, _event: &Event, _cache: &Cache) -> Complex<Float> {
        Complex::new(parameters.get(self.pid_re), parameters.get(self.pid_im))
    }

    fn compute_gradient(
        &self,
        _parameters: &Parameters,
        _event: &Event,
        _cache: &Cache,
        gradient: &mut DVector<Complex<Float>>,
    ) {
        if let ParameterID::Parameter(ind) = self.pid_re {
            gradient[ind] = Complex::ONE;
        }
        if let ParameterID::Parameter(ind) = self.pid_im {
            gradient[ind] = Complex::I;
        }
    }
}

/// A complex-valued [`Amplitude`] which just contains two parameters representing its magnitude and
/// phase.
#[derive(Clone)]
pub struct PolarComplexScalar {
    name: String,
    r: ParameterLike,
    pid_r: ParameterID,
    theta: ParameterLike,
    pid_theta: ParameterID,
}

impl PolarComplexScalar {
    /// Create a new [`PolarComplexScalar`] with the given name, magnitude (`r`), and phase (`theta`).
    pub fn new(name: &str, r: ParameterLike, theta: ParameterLike) -> Box<Self> {
        Self {
            name: name.to_string(),
            r,
            pid_r: Default::default(),
            theta,
            pid_theta: Default::default(),
        }
        .into()
    }
}

impl Amplitude for PolarComplexScalar {
    fn register(&mut self, resources: &mut Resources) -> Result<AmplitudeID, LadduError> {
        self.pid_r = resources.register_parameter(&self.r);
        self.pid_theta = resources.register_parameter(&self.theta);
        resources.register_amplitude(&self.name)
    }

    fn compute(&self, parameters: &Parameters, _event: &Event, _cache: &Cache) -> Complex<Float> {
        Complex::from_polar(parameters.get(self.pid_r), parameters.get(self.pid_theta))
    }

    fn compute_gradient(
        &self,
        parameters: &Parameters,
        _event: &Event,
        _cache: &Cache,
        gradient: &mut DVector<Complex<Float>>,
    ) {
        let exp_i_theta = Complex::cis(parameters.get(self.pid_theta));
        if let ParameterID::Parameter(ind) = self.pid_r {
            gradient[ind] = exp_i_theta;
        }
        if let ParameterID::Parameter(ind) = self.pid_theta {
            gradient[ind] = Complex::<Float>::I
                * Complex::from_polar(parameters.get(self.pid_r), parameters.get(self.pid_theta));
        }
    }
}
