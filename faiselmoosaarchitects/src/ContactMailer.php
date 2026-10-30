<?php

declare(strict_types=1);

namespace App;

use PHPMailer\PHPMailer\Exception as MailException;
use PHPMailer\PHPMailer\PHPMailer;

/**
 * Builds and sends the contact-form email through SMTP.
 *
 * Every connection detail comes from the environment (see .env.example), so
 * the same code talks to Mailpit locally and to the real SMTP host in
 * production without modification.
 */
final class ContactMailer
{
    /**
     * @param array{name:string,email:string,tel:string,subject:string,message:string} $data
     * @throws MailException|\RuntimeException
     */
    public function send(array $data): void
    {
        $mail = new PHPMailer(true);
        $mail->CharSet = PHPMailer::CHARSET_UTF8;

        $mail->isSMTP();
        $mail->Host = Env::require('MAIL_HOST');
        $mail->Port = (int) Env::get('MAIL_PORT', '587');

        $user = Env::get('MAIL_USERNAME');
        $pass = Env::get('MAIL_PASSWORD');
        $mail->SMTPAuth = $user !== null;
        if ($mail->SMTPAuth) {
            $mail->Username = $user;
            $mail->Password = (string) $pass;
        }

        $mail->SMTPSecure = match (strtolower(Env::get('MAIL_ENCRYPTION', 'tls'))) {
            'ssl', 'smtps' => PHPMailer::ENCRYPTION_SMTPS,
            'tls', 'starttls' => PHPMailer::ENCRYPTION_STARTTLS,
            default => '',
        };
        $mail->SMTPAutoTLS = $mail->SMTPSecure !== '';
        $mail->Timeout = (int) Env::get('MAIL_TIMEOUT', '15');

        if (Env::get('MAIL_DEBUG') === '1') {
            $mail->SMTPDebug = 2;
            $mail->Debugoutput = 'error_log';
        }

        // Envelope: From must be a mailbox the SMTP server allows; the visitor
        // goes in Reply-To so replying from the inbox reaches them.
        $mail->setFrom(Env::require('MAIL_FROM_ADDRESS'), Env::get('MAIL_FROM_NAME', 'Website'));
        foreach (array_filter(array_map('trim', explode(',', Env::require('MAIL_TO_ADDRESS')))) as $to) {
            $mail->addAddress($to);
        }
        $mail->addReplyTo($data['email'], $data['name']);

        $subjectPrefix = Env::get('MAIL_SUBJECT_PREFIX', '[Website enquiry]');
        $mail->Subject = trim("$subjectPrefix {$data['subject']} – {$data['name']}");

        $mail->isHTML(true);
        $mail->Body = $this->htmlBody($data);
        $mail->AltBody = $this->textBody($data);

        $mail->send();
    }

    /** @param array<string,string> $d */
    private function textBody(array $d): string
    {
        return "New enquiry from the Faisel Moosa Architects website\n\n"
            . "Name:    {$d['name']}\n"
            . "Email:   {$d['email']}\n"
            . "Phone:   " . ($d['tel'] !== '' ? $d['tel'] : '-') . "\n"
            . "Subject: {$d['subject']}\n\n"
            . "Message:\n{$d['message']}\n\n"
            . "Sent " . date('Y-m-d H:i T') . " from " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown IP') . "\n";
    }

    /** @param array<string,string> $d */
    private function htmlBody(array $d): string
    {
        $e = static fn (string $s): string => htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
        $row = static fn (string $k, string $v): string =>
            "<tr><td style=\"padding:6px 12px 6px 0;color:#666;white-space:nowrap;vertical-align:top\">$k</td>"
            . "<td style=\"padding:6px 0;color:#111\">$v</td></tr>";

        return '<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.5;color:#111;max-width:640px">'
            . '<h2 style="margin:0 0 16px;font-size:18px;color:#906E50">New enquiry from the website</h2>'
            . '<table style="border-collapse:collapse">'
            . $row('Name', $e($d['name']))
            . $row('Email', '<a href="mailto:' . $e($d['email']) . '">' . $e($d['email']) . '</a>')
            . $row('Phone', $d['tel'] !== '' ? $e($d['tel']) : '&ndash;')
            . $row('Subject', $e($d['subject']))
            . '</table>'
            . '<h3 style="margin:20px 0 8px;font-size:15px;color:#666">Message</h3>'
            . '<div style="white-space:pre-wrap;border-left:3px solid #e8ba55;padding:8px 12px;background:#faf8f6">' . $e($d['message']) . '</div>'
            . '<p style="margin-top:20px;font-size:12px;color:#999">Sent ' . $e(date('Y-m-d H:i T')) . ' from ' . $e($_SERVER['REMOTE_ADDR'] ?? 'unknown IP') . '</p>'
            . '</div>';
    }
}
