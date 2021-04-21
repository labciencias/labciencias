let SRV_UUID = 0xDEAD;
let RX_UUID = 0xBEEF;
let TX_UUID = 0xFEED;
let dispositivo, ble_rx, ble_tx;

async function conectar_ble() {  
  dispositivo = await navigator.bluetooth
    .requestDevice({ 
      filters: [{namePrefix: 'Sensor',}],
      optionalServices: [SRV_UUID] 
    });
  let servidor = await dispositivo.gatt.connect();
  let servico = await servidor.getPrimaryService(SRV_UUID);
  ble_rx = await servico.getCharacteristic(RX_UUID);
  ble_tx = await servico.getCharacteristic(TX_UUID);

  await ble_tx.startNotifications();
  ble_tx.addEventListener('characteristicvaluechanged', handleNotifications);

  return dispositivo
};

async function desconectar_ble(){
  await dispositivo.gatt.disconnect();
  dispositivo = null;
  ble_rx = null;
};

function handleNotifications(ev){
  let data = event.target.value;
  let decode = new TextDecoder();
  value = decode.decode(data)
  document.getElementById('in_x').value = value;
};

function ble_write_value(){
  let encoder = new TextEncoder('utf-8');
  value = encoder.encode('1')
  ble_rx.writeValue(value);
};

