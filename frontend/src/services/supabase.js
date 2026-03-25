import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

export const authService = {
  // Sign up
  signUp: (email, password) =>
    supabase.auth.signUp({
      email,
      password,
    }),

  // Sign in
  signIn: (email, password) =>
    supabase.auth.signInWithPassword({
      email,
      password,
    }),

  // Sign out
  signOut: () =>
    supabase.auth.signOut(),

  // Get current user
  getCurrentUser: async () => {
    const { data, error } = await supabase.auth.getUser();
    return { user: data?.user, error };
  },

  // Watch auth changes
  onAuthStateChanged: (callback) => {
    return supabase.auth.onAuthStateChange(callback);
  },

  // Password reset
  resetPassword: (email) =>
    supabase.auth.resetPasswordForEmail(email),

  // Update user
  updateUser: (updates) =>
    supabase.auth.updateUser(updates),
};

export default supabase;
