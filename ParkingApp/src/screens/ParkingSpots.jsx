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
} from 'react-native';
import apiClient from '../api/client';

const ParkingSpots = () => {
  const [spots, setSpots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchSpots = async () => {
    try {
      const response = await apiClient.get('/api/parking/spots');
      setSpots(response.data);
    } catch (error) {
      Alert.alert('Error', 'No se pudieron cargar los espacios');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchSpots();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchSpots();
  };

  const toggleSpot = async (id, occupied) => {
    try {
      const endpoint = occupied ? 'free' : 'occupy';
      await apiClient.post(`/api/parking/spots/${id}/${endpoint}`);
      fetchSpots();
    } catch (error) {
      Alert.alert('Error', 'No se pudo actualizar el espacio');
    }
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={[styles.spotCard, item.occupied ? styles.occupied : styles.free]}
      onPress={() => toggleSpot(item.id, item.occupied)}
    >
      <Text style={styles.spotSlot}>{item.slot}</Text>
      <Text style={styles.spotStatus}>
        {item.occupied ? '🟥 Ocupado' : '🟩 Libre'}
      </Text>
    </TouchableOpacity>
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
      <Text style={styles.title}>🅿️ Espacios de Estacionamiento</Text>
      <FlatList
        data={spots}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        numColumns={2}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={styles.list}
      />
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
  spotCard: {
    flex: 1,
    margin: 8,
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  free: {
    backgroundColor: '#e8f5e9',
    borderWidth: 2,
    borderColor: '#4caf50',
  },
  occupied: {
    backgroundColor: '#ffebee',
    borderWidth: 2,
    borderColor: '#f44336',
  },
  spotSlot: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  spotStatus: {
    fontSize: 14,
    fontWeight: '600',
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default ParkingSpots;
