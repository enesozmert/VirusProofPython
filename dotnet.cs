using System;
using System.Data.SqlClient;

class Program
{
    static void Main(string[] args)
    {
        // Veritabanı bağlantı bilgileri
        string connectionString = "Server=94.154.34.227;Database=VirusProofs;User Id=vpdbsecure;Password=lqT1*XTC#@p=1Ke.PaOZ1_m_%ynd&;TrustServerCertificate=True";

        try
        {
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();
                Console.WriteLine("Veritabanı bağlantısı başarılı!");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Veritabanı bağlantısında hata oluştu: {ex.Message}");
        }
    }
}