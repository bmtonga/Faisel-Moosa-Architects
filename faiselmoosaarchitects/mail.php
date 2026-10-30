<?php

declare(strict_types=1);

/**
 * Contact form handler – Faisel Moosa Architects.
 *
 * Receives the POST from contact-us.html (via assets/js/vendor/ajax-form.js),
 * validates it, and sends it through SMTP with PHPMailer. All mail settings
 * come from environment variables; see .env.example. Nothing in this file
 * changes between local development and production.
 *
 * Responses are plain text: HTTP 200 on success (ajax-form.js shows the text
 * as a success message), 4xx/5xx with a short explanation otherwise.
 */

use App\ContactMailer;
use App\Env;

require __DIR__ . '/vendor/autoload.php';

header('Content-Type: text/plain; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

Env::load(__DIR__);

$respond = static function (int $status, string $message): never {
    http_response_code($status);
    echo $message;
    exit;
};

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    $respond(405, 'Method not allowed.');
}

// Honeypot: real visitors never see or fill this field.
if (trim((string) ($_POST['website'] ?? '')) !== '') {
    $respond(200, 'Thank you – your message has been sent.');
}

$field = static fn (string $key): string => trim(strip_tags((string) ($_POST[$key] ?? '')));

$data = [
    'name'    => $field('lname'),
    'email'   => $field('email'),
    'tel'     => $field('tel'),
    'subject' => $field('subject'),
    'message' => trim((string) ($_POST['textarea'] ?? '')),
];

$errors = [];
if ($data['name'] === '' || mb_strlen($data['name']) > 100) {
    $errors[] = 'Please enter your name.';
}
if (filter_var($data['email'], FILTER_VALIDATE_EMAIL) === false || mb_strlen($data['email']) > 254) {
    $errors[] = 'Please enter a valid email address.';
}
if ($data['tel'] !== '' && !preg_match('/^[0-9+()\s.-]{6,30}$/', $data['tel'])) {
    $errors[] = 'Please enter a valid phone number.';
}
if ($data['subject'] === '' || mb_strlen($data['subject']) > 120) {
    $data['subject'] = 'General enquiry';
}
if (mb_strlen($data['message']) < 10) {
    $errors[] = 'Please tell us a little more about your project (at least 10 characters).';
}
if (mb_strlen($data['message']) > 5000) {
    $errors[] = 'Your message is too long (5000 characters max).';
}
// Header-injection guard: no line breaks in single-line fields.
foreach (['name', 'email', 'tel', 'subject'] as $k) {
    if (preg_match('/[\r\n]/', $data[$k])) {
        $errors[] = 'Invalid characters in the form.';
        break;
    }
}

if ($errors !== []) {
    $respond(422, implode(' ', $errors));
}

try {
    (new ContactMailer())->send($data);
} catch (\Throwable $e) {
    error_log('[contact-form] ' . $e->getMessage());
    $respond(500, 'Sorry, your message could not be sent right now. Please email us directly at '
        . (Env::get('MAIL_TO_ADDRESS') ?? 'our address') . '.');
}

$respond(200, 'Thank you – your message has been sent. We will get back to you shortly.');
