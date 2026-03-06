export interface Farmer {
  farmer_id: string;
  phone_number: string;
  preferred_language: string;
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface Plot {
  plot_id: string;
  farmer_id: string;
  latitude: number;
  longitude: number;
  area_hectares: number;
  crop_types: string[];
  planting_date: string;
  created_at: string;
  updated_at: string;
}

export interface PlotFormData {
  latitude: number;
  longitude: number;
  area_hectares: number;
  crop_types: string[];
  planting_date: string;
}

export interface FarmerFormData {
  phone_number: string;
  preferred_language: string;
  timezone: string;
  plot: PlotFormData;
}

export const SUPPORTED_LANGUAGES = [
  { code: 'hi', name: 'Hindi' },
  { code: 'en', name: 'English' },
  { code: 'te', name: 'Telugu' },
  { code: 'ta', name: 'Tamil' },
  { code: 'kn', name: 'Kannada' },
  { code: 'ml', name: 'Malayalam' },
  { code: 'mr', name: 'Marathi' },
  { code: 'gu', name: 'Gujarati' },
  { code: 'bn', name: 'Bengali' },
  { code: 'pa', name: 'Punjabi' },
];

export const CROP_OPTIONS = [
  'Rice',
  'Wheat',
  'Cotton',
  'Sugarcane',
  'Maize',
  'Pulses',
  'Vegetables',
  'Fruits',
  'Spices',
  'Other',
];
