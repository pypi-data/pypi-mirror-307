use bytes::Bytes;
use ipc_channel::ipc;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct LookupRequest {
    pub resp_channel: ipc::IpcSender<PythonResult>,

    // lookup request
    pub branch: String,
    pub dataset_name: String,
    pub df_keys: Bytes,
    pub series_ts: Bytes,

    pub cols: Vec<String>,

    pub use_asof: bool,

    // timestamp as of the request origination
    pub ts_micros: u64,
}

#[derive(Serialize, Deserialize, Debug)]
pub enum LookupResult {
    Ok((Bytes, Vec<bool>)),
    Err(String),
}

#[derive(Serialize, Deserialize, Debug)]
pub struct MetricBundle {
    // Time (in microseconds) to execute the lookup request.
    pub request_duration: u64,
    // Time (in microseconds) to send the lookup request to the lookup processor.
    pub send_duration: u64,
    // Time (in microseconds) waiting for responses from the lookup processor.
    pub recv_duration: u64,
    // Time (in microseconds) to parse lookup response into Arrow RecordBatch.
    pub parse_rb_duration: u64,
    // Time (in microseconds) to convert the Arrow RecordBatch to PyArrow struct.
    pub pyarrow_convert_duration: u64,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct SecretRequest {
    pub resp_channel: ipc::IpcSender<PythonResult>,

    // secret name
    pub name: String,
    // timestamp as of the request origination
    pub ts_micros: u64,
}

#[derive(Serialize, Deserialize, Debug)]
pub enum SecretResult {
    Ok(String),
    Err(String),
}

#[derive(Serialize, Deserialize, Debug)]
pub enum PythonRequest {
    DatasetLookup(LookupRequest),
    ReportMetrics(MetricBundle),
    Secret(SecretRequest),
}

#[derive(Serialize, Deserialize, Debug)]
pub enum PythonResult {
    DatasetLookup(LookupResult),
    Secret(SecretResult),
}
