-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 10, 2025 at 03:55 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bookstore`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` varchar(120) NOT NULL,
  `category` varchar(50) NOT NULL,
  `price` int(11) NOT NULL,
  `image_url` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `title`, `category`, `price`, `image_url`) VALUES
(1, 'Harry Potter and The Philosopher\'s Stone Minalima Edition', 'Fiction', 739000, 'https://images.tokopedia.net/img/cache/700/VqbcmM/2020/12/5/f1559766-910d-47ae-8965-fabc1d7ec9fb.jpg'),
(2, 'The Phantom of The Opera', 'Fiction', 72000, 'https://storiarts.com/cdn/shop/products/phantom.jpg?v=1642096995'),
(3, 'The Tragedy of Hamlet', 'Classical Fiction', 1200000, 'https://www.jonkers.co.uk/uploads/cache/00055/00055905/00055905-1200x1200.jpeg?v=1'),
(4, 'Romeo and Juliet with illustration by W. Hatherell', 'Classical Fiction', 6650000, 'https://www.jonkers.co.uk/uploads/cache/00062/00062240/00062240-540x540.jpeg?v=1'),
(5, 'Comus illustrated by Arthur Rackham', 'Classical Fiction', 17655000, 'https://www.jonkers.co.uk/uploads/cache/00065/00065744/00065744-900x900.jpeg?v=1'),
(6, 'Cinderella with illustration by Arthur Rackham', 'Classical Fiction', 6600000, 'https://www.jonkers.co.uk/uploads/cache/00082/00082508/00082508-900x900.jpeg?v=1'),
(7, 'Robert Adams and His Brothers: Their Lives, Work, and Influence.', 'Non Fiction', 1650000, 'https://www.jonkers.co.uk/uploads/cache/00084/00084168/00084168-900x900.jpeg?v=1'),
(8, 'The Temple of King Sethos I at Abydos', 'Non Fiction', 99300000, 'https://www.jonkers.co.uk/uploads/cache/00083/00083990/00083990-900x900.jpeg?v=1'),
(9, 'The Path to Power: Margaret Thatcher', 'Biography', 1650000, 'https://www.jonkers.co.uk/uploads/cache/00082/00082620/00082620-540x540.jpeg?v=1'),
(10, 'The Antarctic Manual for the Use of the Expedition of 1901', 'Non Fiction', 165516000, 'https://www.jonkers.co.uk/uploads/cache/00081/00081411/00081411-900x900.jpeg?v=1'),
(11, 'The Marvellous Book', 'Non Fiction', 82758000, 'https://www.jonkers.co.uk/uploads/cache/00046/00046284/00046284-900x900.jpeg?v=1'),
(12, 'Stories From Hans Andersen', 'Fiction', 27586000, 'https://www.jonkers.co.uk/uploads/cache/00075/00075960/00075960-900x900.jpeg?v=1'),
(13, 'Harry Potter Chamber of Secrets Minalima Edition', 'Fiction', 785000, 'https://cdn.media.amplience.net/s/hottopic/31446435_hi'),
(14, 'Harry Potter and The Prisoner of Azkaban Minalima Edition', 'Fiction', 785000, 'https://cdn.media.amplience.net/s/hottopic/31446434_hi'),
(15, 'Tintin and The Picaros', 'Comic', 125000, 'https://www.papertiger.co.uk/cdn/shop/products/dbf347e76bad7fdbd529f0c4ea4ed2bd8c58f1b4_1024x1024.jpg?v=1582822170'),
(16, 'Tintin in The Congo', 'Comic', 125000, 'https://cdn001.tintin.com/public/tintin/img/news/4442/tintin-Congo_coverEN.jpg'),
(17, 'Tintin in America', 'Comic', 125000, 'https://thetintinshop.uk.com/wp-content/uploads/2013/05/English-Books_America1.jpg'),
(18, 'Tintin in the Land of Soviets', 'Comic', 125000, 'https://thetintinshop.uk.com/wp-content/uploads/2013/05/English-Books_Soviets.jpg'),
(19, 'Tintin The Secret of Unicorn', 'Comic', 125000, 'https://thetintinshop.uk.com/wp-content/uploads/2013/05/English-Books_Unicorn.jpg'),
(20, 'Tintin Red Rackham\'s Treassure', 'Comic', 125000, 'https://m.media-amazon.com/images/I/81d-Yenyu0L._AC_UF1000,1000_QL80_.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `cart_items`
--

CREATE TABLE `cart_items` (
  `id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `session_id` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart_items`
--

INSERT INTO `cart_items` (`id`, `book_id`, `quantity`, `session_id`, `user_id`) VALUES
(23, 2, 1, '', 14);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `total_price` float NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(50) NOT NULL DEFAULT 'Unpaid',
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `session_id`, `total_price`, `created_at`, `status`, `user_id`) VALUES
(26, 0, 99300000, '2025-06-09 13:05:46', 'paid', 14),
(27, 0, 1650000, '2025-06-09 13:50:47', 'paid', 15),
(28, 0, 250000, '2025-06-09 14:13:51', 'paid', 15),
(29, 0, 6650000, '2025-06-10 01:42:54', 'paid', 16),
(30, 0, 17655000, '2025-06-10 01:43:30', 'paid', 16),
(31, 0, 84658000, '2025-06-10 01:46:55', 'paid', 17);

-- --------------------------------------------------------

--
-- Table structure for table `orders_item`
--

CREATE TABLE `orders_item` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders_item`
--

INSERT INTO `orders_item` (`id`, `order_id`, `book_id`, `quantity`, `price`) VALUES
(10, 26, 8, 1, 99300000),
(11, 27, 9, 1, 1650000),
(12, 28, 19, 1, 125000),
(13, 28, 20, 1, 125000),
(14, 29, 4, 1, 6650000),
(15, 30, 5, 1, 17655000),
(16, 31, 15, 1, 125000),
(17, 31, 18, 1, 125000),
(18, 31, 11, 1, 82758000),
(19, 31, 9, 1, 1650000);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `phone` int(13) NOT NULL,
  `email` varchar(200) NOT NULL,
  `username` varchar(120) NOT NULL,
  `password` varchar(500) NOT NULL,
  `address` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `phone`, `email`, `username`, `password`, `address`) VALUES
(2, '', 0, '', 'estetika1', 'scrypt:32768:8:1$ZO3QwjkHFIbfUpG5$06e238c7e4ecea6e', ''),
(3, '', 0, '', 'kaka123', 'scrypt:32768:8:1$t9FsQlOAXNv7SmfA$ef9f0c8ed71272b4', ''),
(4, '', 0, '', 'Loli_123', 'scrypt:32768:8:1$Mq8G6RxSa5upbalk$da4ec5e561767d2c', ''),
(5, 'Budi Hartono', 2147483647, 'budi@example.com', 'budi123', 'scrypt:32768:8:1$GU8UaQ1QAk1WDIuk$27434536cf60eac8', 'Jl. Merdeka No. 10'),
(6, '', 0, '', 'silvi', 'pbkdf2:sha256:1000000$Zt9in02LKhCM7hxj$9cdadcd0a6b', ''),
(8, 'Hanasui Power Bright Expert Serum ', 0, 'hana@gmail.com', '', 'pbkdf2:sha256:1000000$8l4fTDwSPwpYfhbV$1116c758bb9', ''),
(9, 'Hanasui Power Bright Expert Serum ', 0, 'hana@gmail.com', '', 'pbkdf2:sha256:1000000$UHrQNC1PYzTa9LqN$32b1a774a58', ''),
(10, 'Hanasui Power Bakuchiol Serum', 0, 'baku@gmail.com', '', 'pbkdf2:sha256:1000000$UXkHhUrc4w2BY1oT$90bb7038936', ''),
(11, 'Hanasui Power Bright Serum', 0, 'bright@gmail.com', '', 'admin', ''),
(12, 'Hanasui Power Bright Expert Serum ', 0, 'bright@gmail.com', '', 'admin', ''),
(13, 'Estetika', 0, 'kaka@gmail.com', '', '123', ''),
(14, 'Joan', 0, 'joan@example.com', '', 'scrypt:32768:8:1$t4Dur7EGL44P6oVK$35699e4ee720801fd21897eaf3041892310b05591211c297e74c5dc46e775e319c5ed07609c43a3849cc7a233bdf47de9b21a5d83f66b083f4f7874171225c24', ''),
(15, 'Lovely Nusantara Yutardo', 812345678, 'loly@example.com', 'lolyonlyloly', 'scrypt:32768:8:1$lu4E1MnKFfXdd7sj$d4723334ab901a00eda71f77c33f7170a0826870f2c26a5575487d03fc0536edc14442c44f172ecd6b7ac4178148331b880acc30bd968d35f78ca2daecc99065', 'Slarongan, 55563'),
(16, 'Budi Hartanto', 2147483647, 'budi@gmail.com', 'budi456', 'scrypt:32768:8:1$z2cDiIOyvvPeHeoO$d5b6ff79e6ca9c388b4d7efb2ec3d56c2c9c5091315819ea96efc0cbbff8c1e82208900785c2e66791fea5bebc60ddb8ad73049e0ab7aeda0810b631349808d1', 'Tambak Bayan IX No, 2C, Caturtunggal, Sleman, DI Y'),
(17, 'Anastasia Silvia ', 2147483647, 'silvi@example.com', 'silvi123', 'scrypt:32768:8:1$fFvVfXvckgUgWlbM$0e11d806b7019fc690e0b9e497cbf961f13012a8889485021386efedf1577d3fff251fcd7c9d7ee727067dc8bcd9996f2fe99cb2dbec6f62a777bfe16b643846', 'Slarongan, Sendangmulyo, Minggir, Sleman, Yogyakar');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_id` (`book_id`),
  ADD KEY `users` (`user_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user` (`user_id`);

--
-- Indexes for table `orders_item`
--
ALTER TABLE `orders_item`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `item_id` (`book_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `cart_items`
--
ALTER TABLE `cart_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `orders_item`
--
ALTER TABLE `orders_item`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD CONSTRAINT `book_id` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  ADD CONSTRAINT `users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orders_item`
--
ALTER TABLE `orders_item`
  ADD CONSTRAINT `item_id` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  ADD CONSTRAINT `order_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
