import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/api/client';
import type { Farmer, Plot, PlotFormData } from '@/types/farmer';

export const useFarmers = () => {
  return useQuery({
    queryKey: ['farmers'],
    queryFn: async () => {
      const response = await apiClient.get<Farmer[]>('/farmers/');
      return response.data;
    },
  });
};

export const useFarmer = (farmerId: string) => {
  return useQuery({
    queryKey: ['farmer', farmerId],
    queryFn: async () => {
      const response = await apiClient.get<Farmer>(`/farmers/${farmerId}`);
      return response.data;
    },
    enabled: !!farmerId,
  });
};

export const useCreateFarmer = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: {
      phone_number: string;
      preferred_language: string;
      timezone: string;
    }) => {
      const response = await apiClient.post<Farmer>('/farmers/', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farmers'] });
    },
  });
};

export const useCreatePlot = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: { farmerId: string; plotData: PlotFormData }) => {
      const response = await apiClient.post<Plot>(
        `/farmers/${data.farmerId}/plots`,
        {
          latitude: data.plotData.latitude,
          longitude: data.plotData.longitude,
          area_hectares: data.plotData.area_hectares,
          crop_types: data.plotData.crop_types,
          planting_date: data.plotData.planting_date,
        }
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farmers'] });
    },
  });
};
