<?php

declare(strict_types=1);

namespace App;

/**
 * Minimal environment loader.
 *
 * Real environment variables (set by the hosting panel, Docker, Apache SetEnv,
 * etc.) always win. A `.env` file in the site root is read only as a fallback,
 * so local development can use one while production never needs it.
 */
final class Env
{
    private static bool $loaded = false;

    /** Load `.env` from $dir once, without overriding variables already set. */
    public static function load(string $dir): void
    {
        if (self::$loaded) {
            return;
        }
        self::$loaded = true;

        $file = rtrim($dir, '/\\') . DIRECTORY_SEPARATOR . '.env';
        if (!is_readable($file)) {
            return;
        }

        foreach (file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [] as $line) {
            $line = trim($line);
            if ($line === '' || str_starts_with($line, '#') || !str_contains($line, '=')) {
                continue;
            }
            [$key, $value] = explode('=', $line, 2);
            $key = trim($key);
            $value = trim($value);

            if (strlen($value) >= 2 && ($value[0] === '"' || $value[0] === "'")) {
                // Quoted value: take what is between the quotes, ignore anything after.
                $quote = $value[0];
                $end = strpos($value, $quote, 1);
                $value = $end === false ? substr($value, 1) : substr($value, 1, $end - 1);
            } elseif (($hash = strpos($value, ' #')) !== false || str_starts_with($value, '#')) {
                // Unquoted value: drop an inline comment.
                $value = trim(substr($value, 0, $hash === false ? 0 : $hash));
            }

            if ($key !== '' && getenv($key) === false && !isset($_ENV[$key])) {
                putenv("$key=$value");
                $_ENV[$key] = $value;
            }
        }
    }

    /** Read a variable; `$default` when unset or empty. */
    public static function get(string $key, ?string $default = null): ?string
    {
        $value = $_ENV[$key] ?? getenv($key);
        if ($value === false || $value === null || $value === '') {
            return $default;
        }
        return (string) $value;
    }

    /** Read a variable that must be present. */
    public static function require(string $key): string
    {
        $value = self::get($key);
        if ($value === null) {
            throw new \RuntimeException("Missing required environment variable: $key");
        }
        return $value;
    }
}
