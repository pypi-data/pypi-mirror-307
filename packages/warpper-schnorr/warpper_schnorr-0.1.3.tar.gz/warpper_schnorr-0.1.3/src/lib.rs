use pyo3::prelude::*;
use sha2::{Digest, Sha256};
use schnorrkel::{signing_context, verify_batch, Keypair};
use rand::{rngs::OsRng, rngs::StdRng, SeedableRng};

pub fn _generate_keys_with_seed(seed: String) -> anyhow::Result<(String, String)> {
    // Hash the seed to create a 32-byte array
    let mut hasher = Sha256::new();
    hasher.update(seed);
    let seed_hash = hasher.finalize();
    let seed_array: [u8; 32] = seed_hash
        .try_into()
        .expect("Hash algorithm changed output size");

    // Generate the key pair
    let mut rng = StdRng::from_seed(seed_array);
    let keypair = Keypair::generate_with(&mut rng);
    let public_key = bs58::encode(keypair.public.to_bytes()).into_string();
    let private_key = bs58::encode(keypair.secret.to_bytes()).into_string();
    Ok((public_key, private_key))
}

#[pyfunction]
fn generate_keys_with_seed (seed: String) -> (String,String){
    let (public_key, private_key) = _generate_keys_with_seed(seed).expect("111");
    (public_key, private_key)
}


fn private_to_public(private_key: String) -> anyhow::Result<String> {
    let private_key_bytes = bs58::decode(private_key).into_vec()?;
    let private_key = schnorrkel::SecretKey::from_bytes(&private_key_bytes)
        .map_err(|_| anyhow::anyhow!("Invalid Schnorr private key"))?;
    let public_key = private_key.to_public();
    Ok(bs58::encode(public_key.to_bytes()).into_string())
}

#[pyfunction]
fn private_key_to_public_key (private_key: String) -> String{
    let result = private_to_public(private_key).expect("111");
    result
}


/// A Python module implemented in Rust.
#[pymodule]
fn warpper_schnorr(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_keys_with_seed, m)?)?;
    m.add_function(wrap_pyfunction!(private_key_to_public_key, m)?)?;
    Ok(())
}

