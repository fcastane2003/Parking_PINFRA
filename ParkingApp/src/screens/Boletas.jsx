import { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  RefreshControl,
  Modal,
  TextInput,
} from 'react-native';
import apiClient from '../api/client';

const Boletas = () => {
  const [boletas, setBoletas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [plate, setPlate] = useState('');
  const [reason, setReason] = useState('');

  const fetchBoletas = async () => {
    try {
      const response = await apiClient.get('/api/boletas');
      setBoletas(response.data);
    } catch (error) {
      Alert.alert('Error', 'No se pudieron cargar las boletas');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchBoletas();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchBoletas();
  };

  const createBoleta = async () => {
    if (!plate) {
      Alert.alert('Error', 'Por favor ingresa la placa');
      return;
    }

    try {
      await apiClient.post('/api/boletas/', {
        plate,
        reason,
        observations: 'Creado desde app móvil',
      });
      setModalVisible(false);
      setPlate('');
      setReason('');
      fetchBoletas();
    } catch (error) {
      Alert.alert('Error', 'No se pudo crear la boleta');
    }
  };

  const renderItem = ({ item }) => (
    <View style={styles.boletaCard}>
      <Text style={styles.boletaFolio}>📄 {item.folio}</Text>
      <Text style={styles.boletaPlate}>🚗 {item.plate}</Text>
      <Text style={styles.boletaState}>
        Estado: {item.state === 'abierta' ? '🟢 Activa' : '🔴 Cerrada'}
      </Text>
      <Text style={styles.boletaDate}>
        {new Date(item.created_at).toLocaleString()}
      </Text>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#1976d2" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>📋 Boletas</Text>

      <TouchableOpacity
        style={styles.addButton}
        onPress={() => setModalVisible(true)}
      >
        <Text style={styles.addButtonText}>+ Nueva Boleta</Text>
      </TouchableOpacity>

      <FlatList
        data={boletas}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={styles.list}
      />

      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Nueva Boleta</Text>

            <TextInput
              style={styles.input}
              placeholder="Placa (ej: ABC-1234)"
              value={plate}
              onChangeText={setPlate}
              autoCapitalize="characters"
            />

            <TextInput
              style={styles.input}
              placeholder="Motivo (opcional)"
              value={reason}
              onChangeText={setReason}
            />

            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={[styles.modalButton, styles.cancelButton]}
                onPress={() => setModalVisible(false)}
              >
                <Text style={styles.modalButtonText}>Cancelar</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.modalButton, styles.confirmButton]}
                onPress={createBoleta}
              >
                <Text style={styles.modalButtonText}>Crear</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  list: {
    paddingBottom: 20,
  },
  boletaCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  boletaFolio: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  boletaPlate: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  boletaState: {
    fontSize: 14,
    marginTop: 4,
  },
  boletaDate: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
  },
  addButton: {
    backgroundColor: '#1976d2',
    padding: 12,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 16,
  },
  addButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContent: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 12,
    width: '85%',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    backgroundColor: '#f5f5f5',
    padding: 12,
    borderRadius: 8,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 12,
  },
  modalButton: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginHorizontal: 4,
  },
  cancelButton: {
    backgroundColor: '#f44336',
  },
  confirmButton: {
    backgroundColor: '#4caf50',
  },
  modalButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});

export default Boletas;
