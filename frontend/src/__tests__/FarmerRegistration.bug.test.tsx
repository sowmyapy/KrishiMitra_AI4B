/**
 * Bug Condition Exploration Test
 * 
 * Property 1: Fault Condition - Complete Registration Creates Both Records
 * 
 * CRITICAL: This test MUST FAIL on unfixed code - failure confirms the bug exists
 * 
 * This test encodes the expected behavior: when a user submits the registration form
 * with complete farmer and plot data, both farmer and plot records should be created.
 * 
 * EXPECTED OUTCOME ON UNFIXED CODE: Test FAILS (proves bug exists)
 * - Only POST /farmers/ is called
 * - No POST /farmers/{farmer_id}/plots call is made
 * - Plot data is discarded
 */

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { SnackbarProvider } from 'notistack';
import { FarmerRegistration } from '../pages/FarmerRegistration';
import { apiClient } from '../api/client';

// Mock the API client
jest.mock('../api/client');
const mockedApiClient = apiClient as jest.Mocked<typeof apiClient>;

// Mock the MapPicker component to avoid Leaflet issues in tests
jest.mock('../components/farmer/MapPicker', () => ({
  MapPicker: ({ onChange, error }: any) => (
    <div data-testid="map-picker">
      <button
        data-testid="set-location"
        onClick={() => onChange({ lat: 28.6139, lng: 77.2090 })}
      >
        Set Location
      </button>
      {error && <span data-testid="map-error">{error}</span>}
    </div>
  ),
}));

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <SnackbarProvider>{children}</SnackbarProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

describe('Bug Condition Exploration: Complete Farmer Registration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('SHOULD create both farmer and plot records when form is submitted with complete data', async () => {
    const user = userEvent.setup();

    // Mock successful farmer creation
    const mockFarmer = {
      farmer_id: 'test-farmer-id-123',
      phone_number: '+918151910856',
      preferred_language: 'hi',
      timezone: 'Asia/Kolkata',
      created_at: new Date().toISOString(),
    };

    mockedApiClient.post.mockResolvedValueOnce({
      data: mockFarmer,
      status: 201,
      statusText: 'Created',
      headers: {},
      config: {} as any,
    });

    // Mock successful plot creation
    const mockPlot = {
      plot_id: 'test-plot-id-456',
      farmer_id: 'test-farmer-id-123',
      latitude: 28.6139,
      longitude: 77.2090,
      area_hectares: 2.5,
      crop_types: ['Rice', 'Wheat'],
      planting_date: '2024-01-15',
      created_at: new Date().toISOString(),
    };

    mockedApiClient.post.mockResolvedValueOnce({
      data: mockPlot,
      status: 201,
      statusText: 'Created',
      headers: {},
      config: {} as any,
    });

    render(<FarmerRegistration />, { wrapper: createWrapper() });

    // Fill in farmer information
    const phoneInput = screen.getByLabelText(/phone number/i);
    await user.type(phoneInput, '+918151910856');

    const languageSelect = screen.getByLabelText(/preferred language/i);
    await user.click(languageSelect);
    const hindiOption = screen.getByRole('option', { name: /hindi/i });
    await user.click(hindiOption);

    // Set farm location using MapPicker
    const setLocationButton = screen.getByTestId('set-location');
    await user.click(setLocationButton);

    // Fill in farm information
    const areaInput = screen.getByLabelText(/farm area/i);
    await user.clear(areaInput);
    await user.type(areaInput, '2.5');

    const cropSelect = screen.getByLabelText(/crop types/i);
    await user.click(cropSelect);
    const riceOption = screen.getByRole('option', { name: /rice/i });
    await user.click(riceOption);
    const wheatOption = screen.getByRole('option', { name: /wheat/i });
    await user.click(wheatOption);
    // Click outside to close dropdown
    await user.click(document.body);

    const plantingDateInput = screen.getByLabelText(/planting date/i);
    await user.type(plantingDateInput, '2024-01-15');

    // Submit the form
    const submitButton = screen.getByRole('button', { name: /register farmer/i });
    await user.click(submitButton);

    // Wait for API calls to complete
    await waitFor(() => {
      expect(mockedApiClient.post).toHaveBeenCalled();
    });

    // ASSERTION 1: POST /farmers/ should be called with farmer data
    expect(mockedApiClient.post).toHaveBeenCalledWith(
      '/farmers/',
      expect.objectContaining({
        phone_number: '+918151910856',
        preferred_language: 'hi',
        timezone: 'Asia/Kolkata',
      })
    );

    // ASSERTION 2: POST /farmers/{farmer_id}/plots should be called with plot data
    // THIS WILL FAIL ON UNFIXED CODE - proving the bug exists
    expect(mockedApiClient.post).toHaveBeenCalledWith(
      '/farmers/test-farmer-id-123/plots',
      expect.objectContaining({
        latitude: 28.6139,
        longitude: 77.2090,
        area_hectares: 2.5,
        crop_types: expect.arrayContaining(['Rice', 'Wheat']),
        planting_date: '2024-01-15',
      })
    );

    // ASSERTION 3: Both API calls should have been made (2 total)
    expect(mockedApiClient.post).toHaveBeenCalledTimes(2);

    // Verify success message is shown
    await waitFor(() => {
      expect(screen.getByText(/farmer registered successfully/i)).toBeInTheDocument();
    });
  });

  it('SHOULD handle farmer creation failure gracefully', async () => {
    const user = userEvent.setup();

    // Mock farmer creation failure
    mockedApiClient.post.mockRejectedValueOnce({
      response: {
        data: { detail: 'Phone number already registered' },
        status: 400,
      },
    });

    render(<FarmerRegistration />, { wrapper: createWrapper() });

    // Fill in minimal form data
    const phoneInput = screen.getByLabelText(/phone number/i);
    await user.type(phoneInput, '+918151910856');

    const languageSelect = screen.getByLabelText(/preferred language/i);
    await user.click(languageSelect);
    const hindiOption = screen.getByRole('option', { name: /hindi/i });
    await user.click(hindiOption);

    const setLocationButton = screen.getByTestId('set-location');
    await user.click(setLocationButton);

    const areaInput = screen.getByLabelText(/farm area/i);
    await user.clear(areaInput);
    await user.type(areaInput, '2.5');

    const cropSelect = screen.getByLabelText(/crop types/i);
    await user.click(cropSelect);
    const riceOption = screen.getByRole('option', { name: /rice/i });
    await user.click(riceOption);
    await user.click(document.body);

    const plantingDateInput = screen.getByLabelText(/planting date/i);
    await user.type(plantingDateInput, '2024-01-15');

    const submitButton = screen.getByRole('button', { name: /register farmer/i });
    await user.click(submitButton);

    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText(/phone number already registered/i)).toBeInTheDocument();
    });

    // Verify only farmer creation was attempted (no plot creation)
    expect(mockedApiClient.post).toHaveBeenCalledTimes(1);
  });
});
